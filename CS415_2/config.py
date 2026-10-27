"""Settings for the two Ollama backends (override with environment variables)."""

import os

BACKENDS: dict[str, dict[str, str]] = {
    # Ollama running on this PC.
    "local": {
        "url": os.getenv("LOCAL_OLLAMA_URL", "http://localhost:11434"),
        # "default_model": os.getenv("LOCAL_MODEL", "qwen2:0.5b"),
        "default_model": os.getenv("LOCAL_MODEL", "qwen2.5-coder:1.5b"),
    },
    # Ollama running on Google Colab, reached through a Cloudflare tunnel.
    # The tunnel URL changes every Colab session: set COLAB_OLLAMA_URL.
    "colab": {
        "url": os.getenv(
            "COLAB_OLLAMA_URL",
            "https://sake-outreach-shoe-retrieval.trycloudflare.com",
        ),
        "default_model": os.getenv("COLAB_MODEL", "llama3.2"),
    },
}

REQUEST_TIMEOUT_SECONDS = 300