import ast
import datetime
import json
import os
from textwrap import dedent, indent
from typing import Optional

from litellm import completion, completion_cost

from rawdog.prompts import script_examples, script_prompt
from rawdog.utils import EnvInfo, rawdog_dir


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

    def __init__(self, config: dict):
        self.log_path = rawdog_dir / "logs.jsonl"

        # In general it's hard to know if the user needs an API key or which environment variables to set
        # We do a simple check here for the default case (gpt- models from openai).
        self.config = config
        if "gpt-" in config.get("llm_model"):
            env_api_key = os.getenv("OPENAI_API_KEY")
            config_api_key = config.get("llm_api_key")
            if config_api_key:
                os.environ["OPENAI_API_KEY"] = config_api_key
            elif not env_api_key:
                print(
                    "It looks like you're using a GPT model without an API key. "
                    "You can add your API key by setting the OPENAI_API_KEY environment variable "
                    "or by adding an llm_api_key field to ~/.rawdog/config.yaml. "
                    "If this was intentional, you can ignore this message."
                )

        self.conversation = [
            {"role": "system", "content": script_prompt},
            {"role": "system", "content": script_examples},
            {"role": "system", "content": EnvInfo().render_prompt()},
        ]

    def get_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        base_url = self.config.get("llm_base_url")
        model = self.config.get("llm_model")
        temperature = self.config.get("llm_temperature")
        custom_llm_provider = self.config.get("llm_custom_provider")

        log = {
            "model": model,
            "prompt": messages[-1]["content"],
            "response": None,
            "cost": None,
        }
        try:
            response = completion(
                base_url=base_url,
                model=model,
                messages=messages,
                temperature=float(temperature),
                custom_llm_provider=custom_llm_provider,
            )
            text = (response.choices[0].message.content) or ""
            log["response"] = text
            if custom_llm_provider:
                cost = 0
            else:
                cost = completion_cost(completion_response=response) or 0
            log["cost"] = f"{float(cost):.10f}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            _, script = ("", "") if not text else parse_script(text)
            if script:
                script_filename = self.log_path.parent / f"script_{timestamp}.py"
                metadata = {
                    "model": model,
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
