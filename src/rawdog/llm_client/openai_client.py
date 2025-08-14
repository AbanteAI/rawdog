import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from rawdog.llm_client.base_client import LLMClient
from rawdog.tools import tools, Tool, ToolOutputText, ToolOutputImage

load_dotenv()


def build_openai_tool_schema(tool: Tool) -> dict:
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description,
        "parameters": {
            "type": "object",
            "properties": {
                schema.name: {"type": schema.type, "description": schema.description} for schema in tool.inputs
            },
            "required": [schema.name for schema in tool.inputs if schema.required],
        },
    }


class OpenAIClient(LLMClient):
    def _initialize_client(self, system_prompt: str):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = self.config.get("llm_model")
        self.temperature = self.config.get("llm_temperature")
        self.tools = {t.name: t for t in tools}
        self.messages.append({"role": "system", "content": system_prompt})

    def _step(self):
        response = self.client.responses.create(
            model=self.model,
            input=self.messages,
            tools=[build_openai_tool_schema(tool) for tool in self.tools.values()],
            tool_choice="required",
        )
        # TODO: update cost

        # Extract the assistant message
        function_calls = []
        for content in response.output:
            if content.type == "function_call":
                name = content.name
                assert name in self.tools, f"Tool {name} not found"
                function_call = {
                    "type": "function_call",
                    "id": content.id,
                    "call_id": content.call_id,
                    "name": name,
                    "arguments": content.arguments,
                }
                function_calls.append(function_call)
                self.messages.append(function_call)
            elif content.type == "reasoning":
                self.messages.append(
                    {
                        "type": "reasoning",
                        "id": content.id,
                        "content": content.content,
                        "summary": content.summary,
                    }
                )
        assert function_calls, "No function calls in response"

        # Extract the tool call data
        for tool_use in function_calls:
            tool = self.tools[tool_use["name"]]
            content = tool.run(**json.loads(tool_use["arguments"]))
            if isinstance(content, ToolOutputText):
                self.messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_use["call_id"],
                        "output": content.text,
                    }
                )
            elif isinstance(content, ToolOutputImage):
                image_url = f"data:{content.media_type};{content.type},{content.data}"
                self.messages.extend(
                    [
                        {
                            "type": "function_call_output",
                            "call_id": tool_use["call_id"],
                            "output": "See image",
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_image",
                                    "image_url": image_url,
                                }
                            ],
                        },
                    ]
                )

    def paused(self):
        in_last_function_call_block = False
        for message in self.messages[::-1]:
            # Iterate backwards until we find the last list of function calls
            if message.get("type") == "function_call":
                in_last_function_call_block = True
                if message.get("name") == "wait_for_feedback":
                    # If any of them are wait_for_feedback, we're paused
                    return True
            elif in_last_function_call_block:
                # If we make it past the last function calls, we're not paused
                break
        return False
