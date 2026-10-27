"""Application entry point for the Ollama chat API."""

from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="Ollama Chat API",
    description="Talk to Ollama running locally or on Google Colab.",
    version="1.0.0",
)

app.include_router(router)