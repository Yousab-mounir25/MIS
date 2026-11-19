"""Logic for talking to the backends (no FastAPI routing code here)."""

import requests

from config import BACKENDS, OMNIROUTE_API_KEY, REQUEST_TIMEOUT_SECONDS
from models import ChatRequest, ChatResponse


class OllamaError(Exception):
    """Raised when a backend cannot be reached or returns an error."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def chat_with_ollama(request: ChatRequest) -> ChatResponse:
    """Send the prompt to the selected backend and return the generated text."""

    if request.source == "omniroute":
        return chat_with_omniroute(request)

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


def chat_with_omniroute(request: ChatRequest) -> ChatResponse:
    """Send the prompt to OmniRoute, which decides which model answers.

    OmniRoute speaks the OpenAI Chat Completions format. We ask for a combo
    (e.g. "MIS-router"); the reply's "model" field tells us which real model
    OmniRoute routed the request to.
    """

    if not OMNIROUTE_API_KEY:
        raise OllamaError(
            "OMNIROUTE_API_KEY is not set. Create a key in the OmniRoute "
            "dashboard (API Keys) and set it as an environment variable "
            "before starting the API.",
            500,
        )

    backend = BACKENDS["omniroute"]
    combo = request.model or backend["default_model"]
    url = f"{backend['url'].rstrip('/')}/chat/completions"

    payload = {
        "model": combo,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {OMNIROUTE_API_KEY}"}

    try:
        reply = requests.post(
            url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        reply.raise_for_status()
        data = reply.json()
        text = data["choices"][0]["message"]["content"]
        answered_by = data.get("model") or combo
    except requests.ConnectionError:
        raise OllamaError(
            f"Could not connect to OmniRoute at {url}. "
            "Is the omniroute container running (docker ps)?"
        )
    except requests.Timeout:
        raise OllamaError("OmniRoute timed out.", 504)
    except requests.HTTPError as error:
        status = error.response.status_code
        hint = " Check OMNIROUTE_API_KEY." if status == 401 else ""
        raise OllamaError(
            f"OmniRoute returned {status}: {error.response.text}{hint}"
        )
    except (KeyError, IndexError, ValueError):
        raise OllamaError("Unexpected response format from OmniRoute.")

    return ChatResponse(
        source="omniroute",
        model=answered_by,
        response=text,
        requested_model=combo,
    )
