<template>
  <div class="main-bg">
    <div class="summarizer-card">
      <h1 class="main-title">YouTube Video Summarizer</h1>
      <form @submit.prevent="summarizeVideo" class="summarizer-form">
        <div class="form-section">
          <label for="url" class="label">Paste YouTube URL:</label>
          <div class="centered-bar">
            <input
              id="url"
              v-model="url"
              type="text"
              class="input"
              placeholder="e.g., https://www.youtube.com/watch?v=..."
              required
            />
            <button type="submit" :disabled="loading" class="btn">
              {{ loading ? 'Summarizing...' : 'Summarize' }}
            </button>
          </div>
        </div>
      </form>

      <transition name="fade">
        <div v-if="error" class="error-section">
          {{ error }}
        </div>
      </transition>

      <transition name="fade">
        <div v-if="result" class="result-row">
          <div class="result-section light-bg">
            <div class="result-label">Topic</div>
            <div class="result-content">{{ result.topic_name }}</div>
          </div>
          <div class="result-section light-bg">
            <div class="result-label">Summary</div>
            <div class="result-content justified">
              {{ result.topic_summary }}
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const url = ref('')
const result = ref(null)
const error = ref('')
const loading = ref(false)

async function summarizeVideo() {
  result.value = null
  error.value = ''
  loading.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/summarize/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url.value }),
    })
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'API Error')
    }
    result.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

.main-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}
.summarizer-card {
  background: linear-gradient(120deg, #232526 0%, #414345 100%);
  border-radius: 28px;
  box-shadow: 0 8px 40px 0 rgba(0,0,0,0.28);
  padding: 3.5rem 3rem 2.5rem 3rem;
  max-width: 1100px;
  width: 94vw;
  transition: box-shadow 0.2s;
}
.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 2.3rem;
  text-align: center;
  letter-spacing: 0.5px;
  font-family: inherit;
  text-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.form-section {
  background: linear-gradient(90deg, #f7fafc 60%, #e3e9f0 100%);
  border-radius: 14px;
  padding: 1.7rem 1.5rem 1.2rem 1.5rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 2px 8px rgba(108,99,255,0.09);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.label {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 0.7rem;
  font-weight: 600;
  font-family: inherit;
  text-align: center;
}
.centered-bar {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 1.2rem;
  width: 100%;
  margin-top: 0.2rem;
}
.input {
  flex: 1 1 0;
  min-width: 0;
  max-width: 420px;
  padding: 0.65rem 1rem;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 1.1rem;
  background: #f4f7fa;
  transition: border 0.2s;
  font-family: inherit;
  box-shadow: 0 1px 4px rgba(44,62,80,0.07);
}
.input:focus {
  outline: none;
  border-color: #6c63ff;
  background: #fff;
}
.btn {
  padding: 0.7rem 2.1rem;
  background: linear-gradient(90deg, #ffb347 0%, #ffcc33 100%);
  color: #232526;
  font-size: 1.1rem;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  box-shadow: 0 2px 8px rgba(255,204,51,0.10);
  font-family: inherit;
  letter-spacing: 0.5px;
}
.btn:disabled {
  background: #ffe9b5;
  color: #b3a16b;
  cursor: not-allowed;
}
.error-section {
  margin-top: 1rem;
  background: linear-gradient(90deg, #ffeaea 60%, #fff0f0 100%);
  color: #c0392b;
  border: 1px solid #ffb3b3;
  border-radius: 10px;
  padding: 1rem 1.2rem;
  font-size: 1rem;
  text-align: center;
  font-family: inherit;
  box-shadow: 0 1px 4px rgba(255,100,100,0.08);
}

/* Results layout */
.result-row {
  margin-top: 2.5rem;
  display: flex;
  flex-direction: row;
  background: transparent;
  border-radius: 18px;
  min-height: 220px;
  width: 100%;
  justify-content: space-between;
  gap: 2rem;
}
.result-section {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 2.3rem 2.2rem;
  border-radius: 18px;
  min-width: 0;
  box-shadow: 0 2px 16px rgba(108,99,255,0.07);
  background: none;
}
.light-bg {
  background: linear-gradient(135deg, #f8fafc 0%, #e9f7fd 100%);
  color: #23242b;
  border: 1.5px solid #e0e7ef;
}
.result-label {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffb347;
  margin-bottom: 1.2rem;
  letter-spacing: 0.5px;
  font-family: inherit;
  text-align: left;
  text-shadow: 0 1px 4px rgba(255,179,71,0.09);
}
.result-content {
  font-size: 1.17rem;
  font-family: inherit;
  line-height: 1.7;
  text-align: justify;
  text-justify: inter-word;
  word-break: break-word;
  min-height: 2.5rem;
  color: inherit;
}
.justified {
  text-align: justify;
  text-justify: inter-word;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
@media (max-width: 950px) {
  .summarizer-card {
    padding: 1.2rem 0.5rem;
    max-width: 98vw;
  }
  .result-row {
    flex-direction: column;
    gap: 1.2rem;
  }
  .result-section {
    padding: 1.2rem 1rem;
    min-height: unset;
  }
}
</style>