"""API schemas and utilities for external integrations."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """A single message in conversation history."""
    role: str  # 'user' or 'bot'
    text: str
    timestamp: str


class SessionInfo(BaseModel):
    """Session metadata."""
    session_id: str
    created_at: str
    message_count: int


class ChatRequest(BaseModel):
    """Chat request payload."""
    message: str
    intent: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response payload."""
    type: str  # 'explain', 'quiz', 'summary'
    payload: object
    session_id: str


class HistoryRequest(BaseModel):
    """Request to fetch conversation history."""
    session_id: str
    limit: Optional[int] = 50


class HistoryResponse(BaseModel):
    """Conversation history response."""
    session_id: str
    messages: List[Message]
    total: int


class QuizQuestion(BaseModel):
    """A single quiz question."""
    question: str
    choices: List[str]
    answer: int


class QuizPayload(BaseModel):
    """Quiz response payload."""
    questions: List[QuizQuestion]
