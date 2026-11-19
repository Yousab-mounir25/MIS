"""Pydantic request/response models for the chat API."""

from typing import Literal

from pydantic import BaseModel, Field

Source = Literal["local", "colab", "omniroute"]


class ChatRequest(BaseModel):
    """Represent a prompt sent to one of the backends."""

    prompt: str = Field(min_length=1)
    source: Source = "local"
    model: str | None = Field(
        default=None,
        description=(
            "Model name. Defaults to the backend's default model. "
            "For 'omniroute' this is the combo name (default: MIS-router)."
        ),
    )


class ChatResponse(BaseModel):
    """Represent the model's answer."""

    source: Source
    model: str = Field(description="The model that actually answered.")
    response: str
    requested_model: str | None = Field(
        default=None,
        description="For 'omniroute': the combo that was asked for.",
    )
