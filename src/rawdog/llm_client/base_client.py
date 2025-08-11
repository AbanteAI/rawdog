import datetime
import json

from rawdog import __version__
from rawdog.utils import rawdog_dir


class LLMClient:
    def __new__(cls, config: dict):
        """Route to appropriate LLM client based on model name"""
        if cls is LLMClient:
            model = config.get("llm_model")
            if model.startswith("claude"):
                from rawdog.llm_client.anthropic_client import AnthropicClient

                return AnthropicClient(config)
            else:
                raise ValueError(f"Unsupported model: {model}")

        return super().__new__(cls)

    def __init__(self, config: dict):
        """Initialize common variables"""
        self.config = config
        self.log_id = f"rawdog_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        self.conversation = []
        self.session_cost = 0
        self._initialize_client(system_prompt="You are Rawdog, a helpful assistant.")

    def add_user_message(self, message: list[dict]):
        self.conversation.append({"role": "user", "content": message})

    def add_assistant_message(self, message: list[dict]):
        self.conversation.append({"role": "assistant", "content": message})

    def step(self):
        if self.conversation[-1]["role"] != "user":
            raise ValueError("Can only step after a user message")
        try:
            return self._step()
        finally:
            self._log_conversation()

    def _log_conversation(self):
        with open(rawdog_dir / f"{self.log_id}.json", "w") as f:
            json.dump(
                {
                    "config": self.config,
                    "conversation": self.conversation,
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
