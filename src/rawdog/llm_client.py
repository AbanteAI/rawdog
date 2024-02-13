import json
import os
import re
from textwrap import dedent, indent
from typing import Optional

from litellm import completion, completion_cost

from rawdog.logging import log_conversation
from rawdog.parsing import parse_script
from rawdog.prompts import script_examples, script_prompt
from rawdog.utils import (EnvInfo, get_llm_base_url, get_llm_custom_provider,
                          get_llm_model, get_llm_temperature, rawdog_log_path)

DEFAULT_MODEL = "gpt-4-turbo-preview"


class LLMClient:

    def __init__(self):
        self.base_url = get_llm_base_url()
        self.model = get_llm_model() or DEFAULT_MODEL
        self.custom_provider = get_llm_custom_provider() or None
        self.temperature = get_llm_temperature() or 1.0

        # In general it's hard to know if the user needs an API key or which environment variables to set
        # If they're using the defaults they'll need to set the OPENAI_API_KEY environment variable
        if (
            self.model == DEFAULT_MODEL
            and not self.custom_provider
            and not self.base_url
        ):
            env_api_key = os.getenv("OPENAI_API_KEY")
            if not env_api_key:
                print("Please set the OPENAI_API_KEY environment variable.")
                quit()

        self.conversation = [
            {"role": "system", "content": script_prompt},
            {"role": "system", "content": script_examples},
            {"role": "system", "content": EnvInfo().render_prompt()},
        ]

    def get_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        log = {
            "model": self.model,
            "prompt": messages[-1]["content"],
            "response": None,
            "cost": None,
        }
        try:
            response = completion(
                base_url=self.base_url,
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                custom_llm_provider=self.custom_provider,
            )
            text = (response.choices[0].message.content) or ""
            self.conversation.append({"role": "assistant", "content": text})
            log["response"] = text
            if self.custom_provider:
                cost = 0
            else:
                cost = completion_cost(completion_response=response) or 0
            log["cost"] = f"{float(cost):.10f}"
            metadata = {
                "model": self.model,
                "cost": log["cost"],
            }
            log_conversation(self.conversation, metadata=metadata)
            return text
        except Exception as e:
            log["error"] = str(e)
            print(f"Error:\n", str(log))
            raise e
        finally:
            with open(rawdog_log_path, "a") as f:
                f.write(json.dumps(log) + "\n")

    def get_script(self, prompt: Optional[str] = None):
        if prompt:
            self.conversation.append({"role": "user", "content": prompt})
        response = self.get_response(self.conversation)
        return parse_script(response)
