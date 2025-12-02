"""Unit tests for agent functions."""
import pytest
from fastapi_study_buddy import agent


def test_explain_fallback():
    """Test explain fallback when no OpenAI key."""
    result = agent.explain("photosynthesis", level="basic")
    assert "photosynthesis" in result.lower()
    assert len(result) > 10


def test_summarize_fallback():
    """Test summarize fallback when no OpenAI key."""
    text = "The sky is blue. Water is wet. Grass is green."
    result = agent.summarize(text, sentences=2)
    assert len(result) > 0
    assert result.endswith('.')


def test_summarize_empty():
    """Test summarize with empty text."""
    result = agent.summarize("")
    assert "No text provided" in result


def test_generate_quiz_fallback():
    """Test quiz generation fallback when no OpenAI key."""
    result = agent.generate_quiz("math", count=3)
    assert len(result) == 3
    assert all(isinstance(q, dict) for q in result)
    assert all('question' in q and 'choices' in q for q in result)


def test_wiki_search():
    """Test Wikipedia search tool."""
    result = agent._wiki_search("Python programming language")
    assert isinstance(result, str)
    # result could be empty if offline, so just check it doesn't crash


def test_safe_calculate():
    """Test safe calculator tool."""
    assert agent._safe_calculate("2 + 2") == "4"
    assert agent._safe_calculate("10 / 2") == "5.0"
    assert agent._safe_calculate("2 ** 3") == "8"
    assert "Error" in agent._safe_calculate("import os")  # blocked
