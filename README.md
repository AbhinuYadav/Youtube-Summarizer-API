YouTube Video Summarizer
A full-stack project that lets you paste any YouTube video URL and instantly get a concise, AI-generated summary of its main topic and content. Built with FastAPI (Python), Gemini (Google GenAI), and Vue 3 for a seamless, modern experience.

✨ Features
Paste a YouTube link and get an instant summary

Automatic transcript extraction (English preferred, Hindi fallback)

Gemini LLM-powered summarization for structured, high-quality output

Modern, responsive Vue.js frontend

Clean, secure API for easy integration

🗂️ Project Structure
text
your-project/

│                                                                                                                        
├── app.py                # FastAPI backend (YouTube + Gemini)                                                                                    
├── .env                  # Backend secrets (not tracked by git)      
├── .gitignore            # Ignores all unnecessary files             
├── frontend/             # Vue 3 frontend app                                                                                                                        
│   ├── src/                                                                                                                        
│   │   └── App.vue       # Main UI component                                                                                                                        
│   ├── public/                                                                                                                        
│   ├── package.json                                                                                                                        
│   ├── vite.config.js                                                                                                                        
│   └── .env              # Frontend secrets (not tracked)                                                                                                                  
└── README.md             # This file                                                                                                                        

🚀 Quick Start
1. Backend (FastAPI + Gemini)
Requirements: Python 3.8+, youtube-transcript-api, google-genai, python-dotenv, fastapi, uvicorn

Setup:

bash
pip install fastapi uvicorn youtube-transcript-api google-genai python-dotenv
Create .env in the backend root:

text
GEMINI_API_KEY=your_actual_gemini_api_key_here
Run the backend:

bash
uvicorn app:app --reload
2. Frontend (Vue 3)
Requirements: Node.js (v16+), npm

Setup:

bash
cd frontend
npm install
npm run dev
App runs at http://localhost:5173/

🧑‍💻 Usage
Paste a YouTube URL in the input box.

Click "Summarize".

View the topic and summary side by side in a beautiful, modern interface.

🛡️ Environment Variables
Backend:

.env (never commit this!):

text
GEMINI_API_KEY=your_actual_gemini_api_key_here
Frontend:

.env (optional, for API base URL or frontend secrets)

🗑️ .gitignore
This project’s .gitignore is set to:

Ignore all unnecessary files for both backend and frontend

Track only essential source, config, and example files

Never commit .env, node_modules/, or dist/ folders

📦 Deployment
Deploy FastAPI backend on any Python-compatible server (Heroku, Render, AWS, etc.)

Build Vue frontend with npm run build and serve the dist/ folder as static files

Update frontend API URLs as needed for production

🙏 Credits
FastAPI

Vue.js

YouTube Transcript APIte

Google Gemini API

python-dotenv

Vi

Enjoy your YouTube Summarizer!
