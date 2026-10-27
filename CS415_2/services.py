"""Logic for talking to Ollama (no FastAPI routing code here)."""

import requests

from config import BACKENDS, REQUEST_TIMEOUT_SECONDS
from models import ChatRequest, ChatResponse


class OllamaError(Exception):
    """Raised when a backend cannot be reached or returns an error."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def chat_with_ollama(request: ChatRequest) -> ChatResponse:
    """Send the prompt to the selected backend and return the generated text."""

    backend = BACKENDS[request.source]
    model = request.model or backend["default_model"]
    url = f"{backend['url'].rstrip('/')}/api/chat"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False,
    }
    # Harmless for local; skips the browser warning page if ngrok is used.
    headers = {"ngrok-skip-browser-warning": "true"}

    try:
        reply = requests.post(
            url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        reply.raise_for_status()
        text = reply.json()["message"]["content"]
    except requests.ConnectionError:
        raise OllamaError(
            f"Could not connect to the '{request.source}' Ollama at {url}. "
            "Is it running (and is the Colab tunnel URL still valid)?"
        )
    except requests.Timeout:
        raise OllamaError(f"The '{request.source}' Ollama timed out.", 504)
    except requests.HTTPError as error:
        raise OllamaError(
            f"'{request.source}' Ollama returned {error.response.status_code}: "
            f"{error.response.text}"
        )
    except (KeyError, ValueError):
        raise OllamaError("Unexpected response format from Ollama.")

    return ChatResponse(source=request.source, model=model, response=text)