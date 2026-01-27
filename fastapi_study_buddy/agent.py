"""
Simple agent implementation with Gemini API support.
Provides dynamic AI responses using Google Gemini.
"""

from typing import List
import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

# Gemini environment
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# LangChain imports
try:
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False


def _wiki_search(query: str) -> str:
    if not query:
        return ""
    try:
        s_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1
        }
        r = httpx.get(s_url, params=params, timeout=8.0)
        j = r.json()
        items = j.get("query", {}).get("search", [])
        if not items:
            return ""

        title = items[0]["title"]
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{httpx.utils.quote(title, safe='')}"
        r2 = httpx.get(summary_url, timeout=8.0)
        j2 = r2.json()
        return j2.get("extract", "")
    except Exception:
        return ""


def _safe_calculate(expr: str) -> str:
    import ast
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
        ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv
    )

    try:
        node = ast.parse(expr, mode="eval")
        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                return "Error: unsupported expression"
        result = eval(compile(node, "<string>", "eval"))
        return str(result)
    except Exception as e:
        return f"Error: {e}"


_AGENT_INSTANCE = None


def _create_agent():
    if not LANGCHAIN_AVAILABLE or not GEMINI_KEY:
        return None

    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_KEY,
            temperature=0.5
        )
    except Exception as e:
        print("Gemini LLM init failed:", e)
        return None

    tools = [
        Tool(
            name="wikipedia_search",
            func=_wiki_search,
            description="Search Wikipedia summaries."
        ),
        Tool(
            name="calculator",
            func=_safe_calculate,
            description="Perform safe math calculations."
        )
    ]

    try:
        return initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    except Exception as e:
        print("Agent init failed:", e)
        return None


def _get_agent():
    global _AGENT_INSTANCE
    if _AGENT_INSTANCE is None:
        _AGENT_INSTANCE = _create_agent()
    return _AGENT_INSTANCE


def explain(topic: str, level: str = "basic") -> str:
    topic = topic.strip() or "a topic"

    if GEMINI_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = f"Give a concise definition of {topic}."
            return agent.run(prompt)

    return f"{topic.capitalize()} is a concept explained at a {level} level."


def generate_quiz(topic: str, count: int = 3) -> List[dict]:
    topic = topic.strip() or "general"

    if GEMINI_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = (
                f"Create {count} multiple-choice questions about {topic}. "
                "Return JSON only with: question, choices (4), answer index."
            )
            out = agent.run(prompt)
            try:
                return json.loads(out)
            except Exception:
                return [{"question": out, "choices": [], "answer": 0}]

    return [
        {
            "question": f"What is a concept about {topic}? ({i+1})",
            "choices": [f"Choice {j+1}" for j in range(4)],
            "answer": 0
        }
        for i in range(count)
    ]


def summarize(text: str, sentences: int = 2) -> str:
    text = (text or "").strip()
    if not text:
        return "No text provided."

    if GEMINI_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = f"Summarize this in {sentences} sentences:\n{text}"
            return agent.run(prompt)

    parts = [p.strip() for p in text.split(".") if p.strip()]
    return ". ".join(parts[:sentences]) + "."
