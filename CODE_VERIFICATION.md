# Code Verification Checklist

## Manual Checks (Do these to verify code is correct)

### 1. Check Python Syntax (No Python needed)
- Open each file in VS Code and look for red squiggly lines
- If you see red underlines = syntax error
- If no red underlines = syntax OK

Files to check:
- `fastapi_study_buddy/main.py` — Check for import errors, function definitions
- `fastapi_study_buddy/agent.py` — Check agent initialization, tool definitions
- `fastapi_study_buddy/db.py` — Check SQLite code
- `fastapi_study_buddy/schemas.py` — Check Pydantic models

### 2. Check File Completeness

**fastapi_study_buddy/main.py should have:**
- ✓ `from fastapi import FastAPI, Request, HTTPException`
- ✓ `from . import agent, db, schemas`
- ✓ `app = FastAPI(...)`
- ✓ `@app.get('/', response_class=HTMLResponse)` — index route
- ✓ `@app.post('/api/chat')` — chat route
- ✓ `@app.post('/api/sessions/create')` — session creation
- ✓ `@app.get('/api/sessions/{session_id}')` — session info
- ✓ `@app.post('/api/history')` — history route
- ✓ `@app.delete('/api/sessions/{session_id}')` — session delete
- ✓ `@app.get('/api/ping')` — health check

**fastapi_study_buddy/agent.py should have:**
- ✓ `def explain(topic: str, level: str = 'basic') -> str:`
- ✓ `def generate_quiz(topic: str, count: int = 3) -> List[dict]:`
- ✓ `def summarize(text: str, sentences: int = 2) -> str:`
- ✓ `def _wiki_search(query: str) -> str:`
- ✓ `def _safe_calculate(expr: str) -> str:`
- ✓ `def _create_agent():`

**fastapi_study_buddy/db.py should have:**
- ✓ `def init_db():`
- ✓ `def save_message(session_id: str, role: str, message: str):`
- ✓ `def get_session_history(session_id: str, limit: int = 50):`
- ✓ `def clear_session(session_id: str):`

**fastapi_study_buddy/schemas.py should have:**
- ✓ `class Message(BaseModel):`
- ✓ `class SessionInfo(BaseModel):`
- ✓ `class ChatRequest(BaseModel):`
- ✓ `class ChatResponse(BaseModel):`
- ✓ `class HistoryRequest(BaseModel):`
- ✓ `class HistoryResponse(BaseModel):`

### 3. Check Templates & Static Files

**fastapi_study_buddy/templates/index.html should have:**
- ✓ `<textarea id="msg">` — input field
- ✓ `<div id="messages">` — message display
- ✓ `<button id="send">` — send button
- ✓ `fetch('/api/chat')` — API call
- ✓ `localStorage.getItem('sessionId')` — session tracking

**fastapi_study_buddy/static/style.css should have:**
- ✓ Some CSS rules (at least 5-10 lines)

### 4. Check Config Files

**requirements.txt should have:**
- ✓ fastapi
- ✓ uvicorn[standard]
- ✓ langchain
- ✓ openai
- ✓ python-dotenv
- ✓ httpx
- ✓ wikipedia
- ✓ pytest
- ✓ requests

**Dockerfile should have:**
- ✓ `FROM python:3.11-slim`
- ✓ `WORKDIR /app`
- ✓ `RUN pip install --no-cache-dir -r requirements.txt`
- ✓ `EXPOSE 8000`
- ✓ `CMD ["uvicorn", "fastapi_study_buddy.main:app", ...]`

**Procfile should have:**
- ✓ `web: uvicorn fastapi_study_buddy.main:app --host 0.0.0.0 --port $PORT`

**.gitignore should have:**
- ✓ `.env`
- ✓ `.venv`
- ✓ `__pycache__`
- ✓ `*.db`

### 5. Online Code Quality Check

Go to https://www.python.org/dev/peps/pep-0008/ and manually verify:
- No lines exceed 100 characters
- Indentation is 4 spaces
- Function names are lowercase_with_underscores

---

## If All Above Checks Pass ✓

Your code is ready! Run locally:

```powershell
cd "c:\Users\Prateek Batra\Downloads\paraphraser"
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn fastapi_study_buddy.main:app --reload --host 0.0.0.0 --port 8000
```

Then visit: http://localhost:8000

---

## Quick Issues to Look For

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'fastapi'` | Run `pip install -r requirements.txt` |
| `cannot find module 'agent'` | Check `fastapi_study_buddy/agent.py` exists |
| `SyntaxError` on line X | Check file in VS Code for red squiggles |
| `TemplateNotFound: index.html` | Check `fastapi_study_buddy/templates/index.html` exists |
| `Database is locked` | Delete `conversations.db` and restart |

