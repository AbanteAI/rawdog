from __future__ import annotations

import datetime
import json
from typing import Tuple

from rawdog import __version__
from rawdog.utils import rawdog_dir


def get_model(model: str) -> Tuple[str, "LLMClient"]:
    """Get the full model name and choose the correct client"""
    anthropic_models = {
        "claude": "claude-sonnet-4-20250514",
        "claude-sonnet-4": "claude-sonnet-4-20250514",
        "claude-opus-4-1-20250805": "claude-opus-4-1-20250805",
        "claude-opus-4-20250514": "claude-opus-4-20250514",
        "claude-sonnet-4-20250514": "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
        "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307": "claude-3-haiku-20240307",
    }

    openai_models = {
        "gpt-4o": "gpt-4o-2024-08-06",
        "gpt-5": "gpt-5-2025-08-07",
        "gpt-5-2025-08-07": "gpt-5-2025-08-07",
        "gpt-5-mini-2025-08-07": "gpt-5-mini-2025-08-07",
        "gpt-5-nano-2025-08-07": "gpt-5-nano-2025-08-07",
        "gpt-4o-2024-08-06": "gpt-4o-2024-08-06",
        "o3-mini": "o3-mini",
        "o3": "o3",
    }

    if model in anthropic_models:
        from rawdog.llm_client.anthropic_client import AnthropicClient
        return anthropic_models[model], AnthropicClient
    elif model in openai_models:
        from rawdog.llm_client.openai_client import OpenAIClient
        return openai_models[model], OpenAIClient
    else:
        raise ValueError(f"Unsupported model: {model}")
    

class LLMClient:
    def __new__(cls, config: dict):
        """Route to appropriate LLM client based on model name"""
        if cls is LLMClient:
            model = config.get("llm_model")
            model_name, client_class = get_model(model)
            config["llm_model"] = model_name
            return client_class(config)

        return super().__new__(cls)

    def __init__(self, config: dict):
        """Initialize common variables"""
        self.config = config
        self.log_id = f"rawdog_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        self.messages = []
        self.session_cost = 0
        self._initialize_client(system_prompt="You are Rawdog, a helpful assistant.")

    def add_user_message(self, message: list[dict]):
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": message})

    def step(self):
        try:
            return self._step()
        finally:
            self._log_conversation()

    def _log_conversation(self):
        with open(rawdog_dir / f"{self.log_id}.json", "w") as f:
            json.dump(
                {
                    "config": self.config,
                    "messages": self.messages,
                    "version": __version__,
                },
                f,
            )

    def _initialize_client(self, system_prompt: str):
        """Ensure configuration is valid, check for API keys, etc."""
        raise NotImplementedError("Subclasses must implement this method")

    def _step(self):
        """Call client, parse and process the response, add to conversation."""
        raise NotImplementedError("Subclasses must implement this method")

    def _paused(self):
        """Return True if it's the user's turn to respond"""
        raise NotImplementedError("Subclasses must implement this method")
