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
    set_base_url,
    set_llm_api_key,
    set_llm_model
)
from rawdog.prompts import (
    continuation_prompt, 
    continuation_examples, 
    script_prompt, 
    script_examples
)


class LLMClient:

    def __init__(self, continuation: bool = False):    
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
        _prompt = continuation_prompt if continuation else script_prompt
        _examples = continuation_examples if continuation else script_examples
        self.conversation = [
            {"role": "system", "content": _prompt},
            {"role": "system", "content": _examples},
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
                api_key=self.api_key,
                model=self.model,
                messages=messages,
                temperature=1.0,
            )
            text = (response.choices[0].message.content) or ""
            log["response"] = text
            cost = completion_cost(completion_response=response) or 0
            log["cost"] = f"{float(cost):.10f}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            script_filename = self.log_path.parent / f"script_{timestamp}.py"

            script = None if not text else re.search(r'```(.*?)```', text, re.DOTALL)
            script_content = dedent(f"""\
                # Model: {log['model']}
                # Prompt: {log['prompt']}
                # Response Cost: {log.get('cost', 'N/A')}
                """) + script.group(1) if script else f"INVALID SCRIPT:\n{text}"
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
        
    def get_script(self, prompt: str):
        self.conversation.append({"role": "user", "content": f"PROMPT: {prompt}"})
        response = self.get_response(self.conversation)
        self.conversation.append({"role": "system", "content": response})

        # Parse script from response
        error = None
        script = None
        if response.count("```") > 1:
            script = re.search(r'```(.*?)```', response, re.DOTALL)
            if not script:
                error = f"No script found in response: {response}"
            script = script.group(1)
            script = dedent(script).strip()
            if script.split("\n")[0].startswith("python"):
                script = "\n".join(script.split("\n")[1:])
            # Make sure it isn't json
            try:
                script = json.loads(script)
            except Exception as e:
                pass
            # Make sure it's valid python
            try:
                ast.parse(script)
            except SyntaxError as e:
                error == f"Invalid script:\n{script}"
                script = None
        else:
            error = f"No script found in response: {response}"
        return error, script
