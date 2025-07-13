import os
import re
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; use a specific origin in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_youtube_id(url):
    """
    Extracts the YouTube video ID from different URL formats.
    Returns the video ID as a string, or None if not found.
    """
    pattern = r"(?:youtube\.com/(?:.*v=|.*\/(?:embed|v|shorts)/)|youtu\.be/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_youtube_transcript(video_id):
    """
    Try to fetch the transcript in English, then Hindi if English is not available.
    Returns transcript text or None if not available.
    """
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        except NoTranscriptFound:
            return None
    return "\n".join([entry['text'] for entry in transcript])

def call_gemini_with_transcript(transcript_text):
    """
    Send transcript to Gemini for summarization in JSON format.
    Returns a Python dict with topic_name and topic_summary.
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Based on above Youtube transcription return me breif transcription of its summary in given JSON format:

{
"topic_name":"name of topic"
"topic_summary":"summary of topic"
}"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""I need the YouTube transcription to provide you with the JSON format you requested. Please provide the transcription text so I can create the summary and format it correctly.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=transcript_text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.5,
        response_mime_type="text/plain",
    )
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    # Try parsing the response as JSON
    try:
        summary_json = json.loads(response.text)
    except json.JSONDecodeError:
        # Extract JSON object from text if Gemini returns extra text
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            summary_json = json.loads(match.group(0))
        else:
            raise ValueError("Could not extract JSON from Gemini response.")
    return summary_json

class YouTubeURLRequest(BaseModel):
    url: str

@app.post("/summarize/")
async def summarize_youtube_video(request: YouTubeURLRequest):
    video_id = extract_youtube_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL or video ID not found.")
    transcript = get_youtube_transcript(video_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found in English or Hindi.")
    try:
        summary_json = call_gemini_with_transcript(transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini summarization failed: {str(e)}")
    return summary_json
