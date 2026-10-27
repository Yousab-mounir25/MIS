"""Pydantic request/response models for the Ollama chat API."""

from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Represent a prompt sent to one of the Ollama backends."""

    prompt: str = Field(min_length=1)
    source: Literal["local", "colab"] = "local"
    model: str | None = Field(
        default=None,
        description="Model name. Defaults to the backend's default model.",
    )


class ChatResponse(BaseModel):
    """Represent the model's answer."""

    source: Literal["local", "colab"]
    model: str
    response: str