"""SQLite persistence for conversation history."""
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'conversations.db')


def init_db():
    """Initialize database with conversations table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, message: str):
    """Save a message (user or bot) to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO conversations (session_id, role, message, created_at) VALUES (?, ?, ?, ?)',
        (session_id, role, message, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def get_session_history(session_id: str, limit: int = 50) -> List[Tuple[str, str, str]]:
    """Retrieve conversation history for a session (role, message, timestamp)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'SELECT role, message, created_at FROM conversations WHERE session_id = ? ORDER BY created_at DESC LIMIT ?',
        (session_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))


def clear_session(session_id: str):
    """Clear all messages for a session."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()
