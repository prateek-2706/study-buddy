"""Integration tests for FastAPI routes."""
from fastapi.testclient import TestClient
from fastapi_study_buddy.main import app

client = TestClient(app)


def test_get_index():
    """Test GET / returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Study Buddy" in response.text


def test_ping():
    """Test GET /api/ping."""
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_post_chat_explain():
    """Test POST /api/chat with explain intent."""
    response = client.post("/api/chat", json={"message": "explain: photosynthesis"})
    assert response.status_code == 200
    data = response.json()
    assert 'type' in data
    assert 'payload' in data


def test_post_chat_quiz():
    """Test POST /api/chat with quiz intent."""
    response = client.post("/api/chat", json={"message": "quiz: calculus"})
    assert response.status_code == 200
    data = response.json()
    assert data['type'] == 'quiz'
    assert isinstance(data['payload'], list)


def test_post_chat_summarize():
    """Test POST /api/chat with summarize intent."""
    response = client.post("/api/chat", json={"message": "summarize: The sun is bright. The moon is dark."})
    assert response.status_code == 200
    data = response.json()
    assert data['type'] == 'summary'
    assert isinstance(data['payload'], str)
