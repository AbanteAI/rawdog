import ast
import datetime
import json
import os
import re
from textwrap import dedent

from litellm import completion, completion_cost

from rawdog.utils import (
    rawdog_dir, 
    get_llm_base_url, 
    get_llm_api_key, 
    get_llm_model,
    get_llm_custom_provider,
    set_base_url,
    set_llm_api_key,
    set_llm_model,
    set_llm_custom_provider
)
from rawdog.prompts import script_prompt, script_examples


def parse_script(response: str) -> tuple[str, str]:
    """Split the response into a message and a script.
    
    Expected use is: run the script if there is one, otherwise print the message.
    """
    # Parse delimiter
    n_delimiters = response.count("```")
    if n_delimiters < 2:
        return f"Error: No script found in response:\n{response}", ""
    segments = response.split("```")
    message = f'{segments[0]}\n{segments[-1]}'
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
        self.base_url = get_llm_base_url() or 'https://api.openai.com/v1'
        set_base_url(self.base_url)
        self.model = get_llm_model() or 'gpt-4'
        set_llm_model(self.model)
        self.api_key = get_llm_api_key() or os.environ.get("OPENAI_API_KEY")
        while self.api_key is None:
            print(f"API Key ({self.api_key}) not found. ")
            self.api_key = input("Enter API Key (e.g. OpenAI): ").strip()
            set_llm_api_key(self.api_key)
        self.custom_provider = get_llm_custom_provider() or None
        set_llm_custom_provider(self.custom_provider)
        self.conversation = [
            {"role": "system", "content": script_prompt},
            {"role": "system", "content": script_examples},
        ]

    def get_response(
        self, 
        messages: list[dict[str, str]],
        temperature: float=1.0,
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
                api_key=self.api_key,
                model=self.model,
                messages=messages,
                temperature=temperature,
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
            script_filename = self.log_path.parent / f"script_{timestamp}.py"
            _, script = ("", "") if not text else parse_script(text)
            script_content = dedent(f"""\
                # Model: {log['model']}
                # Prompt: {log['prompt']}
                # Response Cost: {log.get('cost', 'N/A')}
                """) + script if script else f"INVALID SCRIPT:\n{text}"
            with open(script_filename, "w") as script_file:
                script_file.write(script_content)
            return text
        except Exception as e:
            log["error"] = str(e)
            print(f"Error:\n", str(log))
            raise e
        finally:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(log) + "\n")
        
    def get_script(self, prompt: str, temperature: float=1.0):
        self.conversation.append({"role": "user", "content": f"PROMPT: {prompt}"})
        response = self.get_response(self.conversation, temperature)
        self.conversation.append({"role": "system", "content": response})
        return parse_script(response)
