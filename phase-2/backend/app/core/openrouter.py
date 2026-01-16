"""OpenRouter client configuration for Phase III AI Chatbot."""

import os
from functools import wraps

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

def get_client():
    """Get OpenRouter client, initializing only when called."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": os.getenv("BACKEND_URL", "http://localhost:8000"),
            "X-Title": "Todo App Phase III"
        }
    )


# For backward compatibility, define client as a property that initializes on first access
class _LazyClient:
    def __init__(self):
        self._client = None

    def __getattr__(self, name):
        if self._client is None:
            self._client = get_client()
        return getattr(self._client, name)


client = _LazyClient()


def retry_on_rate_limit(func):
    """Decorator to retry on rate limit errors."""
    @wraps(func)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper


# Example usage function
async def call_openrouter(messages, functions=None, function_call="auto"):
    """Call OpenRouter API with retry logic."""
    kwargs = {
        "model": MODEL,
        "messages": messages,
        "timeout": 10.0
    }

    if functions:
        kwargs["functions"] = functions
        kwargs["function_call"] = function_call

    return await client.chat.completions.create(**kwargs)