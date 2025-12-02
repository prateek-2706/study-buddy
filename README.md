# Study Buddy — FastAPI Agentic AI Web App

A conversational Study Buddy web app with LangChain + OpenAI integration. Ask it to explain topics, generate quizzes, and summarize text. Comes with SQLite persistence, tests, and deployment guides.

## Features

- **Explain**: Ask about any topic; get a clear explanation with examples (uses OpenAI GPT + Wikipedia if available).
- **Quiz**: Generate multiple-choice questions to test your knowledge.
- **Summarize**: Paste text and get a concise summary.
- **Persistent Sessions**: Conversation history stored in SQLite per session ID.
- **Fallback mode**: Works without API keys using deterministic logic.
- **Deployment-ready**: Docker, Railway, and Render guides included.

## Quick Start

### Run locally (PowerShell)

```powershell
cd "c:\Users\Prateek Batra\Downloads\paraphraser"
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn fastapi_study_buddy.main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 and try:
- `explain: photosynthesis`
- `quiz: calculus`
- `summarize: <paste your text>`

### Enable OpenAI features

1. Create `.env` in the project root:
```
OPENAI_API_KEY=sk-...
```

2. Restart the app. Agent now uses OpenAI Chat Completions API for richer responses.

## Project Structure

```
fastapi_study_buddy/
├── main.py          # FastAPI routes and session management
├── agent.py         # LangChain agent with tools (wikipedia_search, calculator)
├── db.py            # SQLite persistence
├── templates/
│   └── index.html   # Chat UI
└── static/
    └── style.css    # Minimal styling
tests/
├── test_agent.py    # Unit tests for agent functions
├── test_routes.py   # Integration tests for FastAPI routes
└── conftest.py      # Pytest configuration
```

## API Documentation

All endpoints are documented at **http://localhost:8000/docs** (Swagger UI) when running locally.

### Chat Endpoint
**POST** `/api/chat`

Request:
```json
{
  "message": "explain: photosynthesis",
  "intent": "explain",
  "session_id": "abc123"
}
```

Response:
```json
{
  "type": "explain",
  "payload": "Photosynthesis is...",
  "session_id": "abc123"
}
```

### Session Management

**POST** `/api/sessions/create` — Create a new session
```bash
curl -X POST http://localhost:8000/api/sessions/create
```

**GET** `/api/sessions/{session_id}` — Get session info
```bash
curl http://localhost:8000/api/sessions/abc123
```

**DELETE** `/api/sessions/{session_id}` — Clear session
```bash
curl -X DELETE http://localhost:8000/api/sessions/abc123
```

### History Endpoint
**POST** `/api/history`

Request:
```json
{
  "session_id": "abc123",
  "limit": 50
}
```

Response:
```json
{
  "session_id": "abc123",
  "messages": [
    {
      "role": "user",
      "text": "explain: photosynthesis",
      "timestamp": "2025-12-03T10:30:00.123456"
    },
    {
      "role": "bot",
      "text": "Photosynthesis is...",
      "timestamp": "2025-12-03T10:30:01.234567"
    }
  ],
  "total": 2
}
```

### Health Check
**GET** `/api/ping`

Response:
```json
{"status": "ok"}
```

---



See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guides for:
- **Railway**: Git-based auto-deploy, environment variables in dashboard.
- **Render**: Similar setup, good for hobby projects.

Key steps:
1. Set `OPENAI_API_KEY` in the platform's environment settings (never commit it).
2. Use build command: `pip install -r requirements.txt`
3. Use start command: `uvicorn fastapi_study_buddy.main:app --host 0.0.0.0 --port $PORT`

## Notes

- Conversations are stored in `conversations.db` (SQLite). On ephemeral platforms (Railway/Render free tier), data is lost on redeploy. Add PostgreSQL for persistence if needed.
- The agent uses two tools by default: **Wikipedia search** (free, no key) and **calculator** (safe arithmetic only). Add SerpAPI key in `.env` for web search (optional).
- Without an OpenAI key, the app still works using simple heuristics (regex intent matching, naive summarization, etc.).

## License & Credits

This is a student project for lab evaluation demonstrating Agentic AI concepts with FastAPI.

---

**Happy learning! 🎓**
