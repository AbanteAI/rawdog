import ast
import datetime
import json
import os
import re
from textwrap import dedent, indent
from typing import Optional

from litellm import completion, completion_cost

from rawdog.prompts import script_examples, script_prompt
from rawdog.utils import (
    EnvInfo,
    get_llm_base_url,
    get_llm_custom_provider,
    get_llm_model,
    get_llm_temperature,
    rawdog_dir,
)


def parse_script(response: str) -> tuple[str, str]:
    """Split the response into a message and a script.

    Expected use is: run the script if there is one, otherwise print the message.
    """
    # Parse delimiter
    n_delimiters = response.count("```")
    if n_delimiters < 2:
        return f"Error: No script found in response:\n{response}", ""
    segments = response.split("```")
    message = f"{segments[0]}\n{segments[-1]}"
    script = "```".join(segments[1:-1]).strip()  # Leave 'inner' delimiters alone

    # Check for common mistakes
    if script.split("\n")[0].startswith("python"):
        script = "\n".join(script.split("\n")[1:])
    try:  # Make sure it isn't json
        script = json.loads(script)
    except Exception as e:
        pass
    try:  # Make sure it's valid python
        ast.parse(script)
    except SyntaxError as e:
        return f"Script contains invalid Python:\n{response}", ""
    return message, script


class LLMClient:

    def __init__(self):
        self.log_path = rawdog_dir / "logs.jsonl"
        self.base_url = get_llm_base_url()
        self.model = get_llm_model() or "gpt-4"
        self.custom_provider = get_llm_custom_provider() or None
        self.temperature = get_llm_temperature() or 1.0

        # In general it's hard to know if the user needs an API key or which environment variables to set
        # If they're using the defaults they'll need to set the OPENAI_API_KEY environment variable
        if self.model == "gpt-4" and not self.custom_provider and not self.base_url:
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
            log["response"] = text
            if self.custom_provider:
                cost = 0
            else:
                cost = completion_cost(completion_response=response) or 0
            log["cost"] = f"{float(cost):.10f}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            _, script = ("", "") if not text else parse_script(text)
            if script:
                script_filename = self.log_path.parent / f"script_{timestamp}.py"
                metadata = {
                    "model": self.model,
                    "cost": log.get("cost", "N/A"),
                    "timestamp": timestamp,
                    "log_version": 0.1,
                }
                script_content = (
                    f"conversation = {json.dumps(messages[2:], indent=4)}\n\n"
                    f"metadata = {json.dumps(metadata, indent=4)}\n\n\n"
                    "def main():\n" + indent(script, "    ") + "\n\n\n"
                )
                script_content += dedent(
                    """\
                            if __name__ == "__main__":
                                main()
                            """
                )
                with open(script_filename, "w") as script_file:
                    script_file.write(script_content)
                latest_script_filename = self.log_path.parent / "latest.py"
                with open(latest_script_filename, "w") as script_file:
                    script_file.write(script_content)
            return text
        except Exception as e:
            log["error"] = str(e)
            print(f"Error:\n", str(log))
            raise e
        finally:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(log) + "\n")

    def get_script(self, prompt: Optional[str] = None):
        if prompt:
            self.conversation.append({"role": "user", "content": prompt})
        response = self.get_response(self.conversation)
        self.conversation.append({"role": "assistant", "content": response})
        return parse_script(response)
