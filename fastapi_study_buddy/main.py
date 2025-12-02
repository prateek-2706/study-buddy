from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import os
import uuid
from datetime import datetime

from . import agent
from . import db
from . import schemas

app = FastAPI(
    title="Study Buddy API",
    description="Agentic AI Study Buddy with LangChain",
    version="1.0.0"
)

# Enable CORS for external integrations
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="fastapi_study_buddy/static"), name="static")
templates = Jinja2Templates(directory="fastapi_study_buddy/templates")

# Initialize database on startup
db.init_db()

# Global sessions tracker
_sessions = {}

@app.post('/api/chat', response_model=schemas.ChatResponse)
async def chat(req: schemas.ChatRequest):
    """Chat endpoint: explain, quiz, or summarize."""
    text = req.message.strip()
    intent = (req.intent or '').lower()
    session_id = req.session_id or str(uuid.uuid4())

    # Track session
    if session_id not in _sessions:
        _sessions[session_id] = {'created_at': datetime.utcnow().isoformat()}

    # Save user message
    db.save_message(session_id, 'user', text)

    # simple intent detection
    if not intent:
        if text.lower().startswith('quiz:'):
            intent = 'quiz'
            text = text[len('quiz:'):].strip()
        elif text.lower().startswith('explain:'):
            intent = 'explain'
            text = text[len('explain:'):].strip()
        elif text.lower().startswith('summarize:'):
            intent = 'summarize'
            text = text[len('summarize:'):].strip()

    if intent == 'quiz':
        payload = agent.generate_quiz(text or 'general')
    elif intent == 'summarize':
        payload = agent.summarize(text or '')
    else:  # default to explain
        payload = agent.explain(text or 'a topic', level='basic')

    # Save bot response
    bot_response = str(payload)
    db.save_message(session_id, 'bot', bot_response)

    # Determine type for response
    resp_type = intent if intent in ['quiz', 'summarize'] else 'explain'
    return schemas.ChatResponse(
        type=resp_type,
        payload=payload,
        session_id=session_id
    )


@app.post('/api/sessions/create')
async def create_session():
    """Create a new session and return session ID."""
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {'created_at': datetime.utcnow().isoformat()}
    return JSONResponse({'session_id': session_id, 'created_at': _sessions[session_id]['created_at']})


@app.get('/api/sessions/{session_id}')
async def get_session(session_id: str):
    """Get session info."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = db.get_session_history(session_id, limit=1000)
    return schemas.SessionInfo(
        session_id=session_id,
        created_at=_sessions[session_id]['created_at'],
        message_count=len(history)
    )


@app.post('/api/history')
async def get_history(req: schemas.HistoryRequest):
    """Get conversation history for a session."""
    history = db.get_session_history(req.session_id, limit=req.limit or 50)
    messages = [
        schemas.Message(role=h[0], text=h[1], timestamp=h[2])
        for h in history
    ]
    return schemas.HistoryResponse(
        session_id=req.session_id,
        messages=messages,
        total=len(messages)
    )


@app.delete('/api/sessions/{session_id}')
async def clear_session(session_id: str):
    """Clear all messages in a session."""
    db.clear_session(session_id)
    if session_id in _sessions:
        del _sessions[session_id]
    return JSONResponse({'status': 'cleared', 'session_id': session_id})


@app.get('/api/ping')
async def ping():
    return JSONResponse({'status': 'ok'})
