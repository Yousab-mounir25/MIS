"""API routes for the Ollama chat API."""

from fastapi import APIRouter, HTTPException

from config import BACKENDS
from models import ChatRequest, ChatResponse
from services import OllamaError, chat_with_ollama

router = APIRouter()


@router.get("/")
def home() -> dict[str, str]:
    """Return a simple API status message."""

    return {"message": "Ollama chat API is running"}


@router.get("/backends")
def list_backends() -> dict[str, dict[str, str]]:
    """Show the available backends and their default models."""

    return {
        name: {"url": cfg["url"], "default_model": cfg["default_model"]}
        for name, cfg in BACKENDS.items()
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Send a prompt to Ollama running locally or on Colab."""

    try:
        return chat_with_ollama(request)
    except OllamaError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message)