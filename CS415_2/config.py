"""Settings for the backends (override with environment variables)."""

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
    # OmniRoute gateway: picks which model answers, based on the combo's
    # routing strategy (e.g. round-robin across the local Ollama models).
    # OpenAI-compatible endpoint; the model name is the combo name.
    "omniroute": {
        "url": os.getenv("OMNIROUTE_URL", "http://localhost:20128/v1"),
        "default_model": os.getenv("OMNIROUTE_MODEL", "MIS-router"),
    },
}

# OmniRoute endpoint key (created in the OmniRoute dashboard → API Keys).
# Read from the environment only — never hard-code it here or commit it.
OMNIROUTE_API_KEY = os.getenv("OMNIROUTE_API_KEY", "")

REQUEST_TIMEOUT_SECONDS = 300
