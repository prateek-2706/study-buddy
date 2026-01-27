"""Simple agent implementation with HuggingFace Inference API support.
This gives dynamic AI responses using HuggingFace models.
If `HF_API_KEY` is set in the environment, the agent will call HuggingFace models.
"""
from typing import List
import os
import httpx
import json

HF_KEY = os.getenv('HF_API_KEY')
HF_MODEL = "meta-llama/Llama-2-7b-chat-hf"
HF_API_URL = "https://api-inference.huggingface.co/models/"

try:
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.llms.huggingface_hub import HuggingFaceHub
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False


def _wiki_search(query: str) -> str:
    """Simple Wikipedia search: returns the first search result summary."""
    if not query:
        return ""
    try:
        # search
        s_url = 'https://en.wikipedia.org/w/api.php'
        params = {'action': 'query', 'list': 'search', 'srsearch': query, 'format': 'json', 'srlimit': 1}
        r = httpx.get(s_url, params=params, timeout=8.0)
        j = r.json()
        items = j.get('query', {}).get('search', [])
        if not items:
            return ''
        title = items[0]['title']
        # fetch summary
        summary_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{httpx.utils.quote(title, safe="")}'
        r2 = httpx.get(summary_url, timeout=8.0)
        j2 = r2.json()
        return j2.get('extract', '')
    except Exception:
        return ''


def _safe_calculate(expr: str) -> str:
    """Evaluate a simple arithmetic expression safely using ast."""
    import ast

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv, ast.LParen, ast.RParen)
    try:
        node = ast.parse(expr, mode='eval')
        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                return 'Error: unsupported expression'
        result = eval(compile(node, '<string>', 'eval'))
        return str(result)
    except Exception as e:
        return f'Error: {e}'


def _create_agent():
    if not LANGCHAIN_AVAILABLE or not HF_KEY:
        return None
    try:
        llm = HuggingFaceHub(
            repo_id=HF_MODEL,
            huggingfacehub_api_token=HF_KEY,
            model_kwargs={'temperature': 0.5, 'max_length': 256}
        )
    except Exception:
        return None

    tools = [
        Tool(name='wikipedia_search', func=_wiki_search, description='Useful for searching Wikipedia summaries for factual information.'),
        Tool(name='calculator', func=_safe_calculate, description='Performs safe arithmetic calculations. Input is a math expression.'),
    ]

    try:
        agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
        return agent
    except Exception:
        return None


_AGENT_INSTANCE = None


def _get_agent():
    global _AGENT_INSTANCE
    if _AGENT_INSTANCE is None:
        _AGENT_INSTANCE = _create_agent()
    return _AGENT_INSTANCE


def explain(topic: str, level: str = 'basic') -> str:
    topic = topic.strip() or 'a topic'

    if HF_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = f"You are a helpful tutor. Explain {topic} with a 50 word definition."
            try:
                return agent.run(prompt)
            except Exception as e:
                return f"(agent-failed) {e}"

    return f"{topic.capitalize()} is a concept explained at a basic level."





def generate_quiz(topic: str, count: int = 3) -> List[dict]:
    topic = topic.strip() or 'general'
    if HF_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = (
                f"Create {count} multiple-choice questions about {topic}. "
                "For each question return: question, choices (array of 4), and the index of the correct answer. "
                "Return only valid JSON."
            )
            try:
                out = agent.run(prompt)
                # try to extract JSON from the output
                try:
                    parsed = json.loads(out)
                    return parsed
                except Exception:
                    # fallback: return single placeholder
                    return [{'question': out, 'choices': [], 'answer': 0}]
            except Exception as e:
                return [{'question': f'(agent-failed) {e}', 'choices': [], 'answer': 0}]

    quizzes = []
    for i in range(count):
        q = f"What is a basic concept about {topic}? (question {i+1})"
        choices = [f"Concept {j+1}" for j in range(4)]
        quizzes.append({'question': q, 'choices': choices, 'answer': 0})
    return quizzes


def summarize(text: str, sentences: int = 2) -> str:
    text = (text or '').strip()
    if not text:
        return 'No text provided to summarize.'
    if HF_KEY and LANGCHAIN_AVAILABLE:
        agent = _get_agent()
        if agent:
            prompt = f"Summarize the following text in {sentences} sentences:\n\n{text}"
            try:
                return agent.run(prompt)
            except Exception as e:
                return f"(agent-failed) {e}"

    parts = text.replace('\n', ' ').split('.')
    parts = [p.strip() for p in parts if p.strip()]
    summary = '. '.join(parts[:sentences])
    if not summary.endswith('.'):
        summary += '.'
    return summary

