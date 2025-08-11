import os

from anthropic import Anthropic
from dotenv import load_dotenv

from rawdog.llm_client.base_client import LLMClient
from rawdog.tools import tools, Tool

load_dotenv()


def build_anthropic_tool_schema(tool: Tool) -> dict:
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": {
            "type": "object",
            "properties": {
                schema.name: {
                    "type": schema.type,
                    "description": schema.description,
                }
                for schema in tool.inputs
            },
            "required": [schema.name for schema in tool.inputs if schema.required],
        },
    }


class AnthropicClient(LLMClient):
    def _initialize_client(self, system_prompt: str):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)
        self.model = self.config.get("llm_model")
        self.temperature = self.config.get("llm_temperature")
        self.tools = {t.name: t for t in tools}
        self.system = system_prompt

    def _step(self):
        # Generate completion
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=self.temperature,
            tools=[build_anthropic_tool_schema(tool) for tool in self.tools.values()],
            system=self.system,
            messages=self.conversation,
            tool_choice={"type": "any"},  # Only allow tool calls
        )
        # TODO: update cost

        # Extract the assistant message
        assistant_message = []
        for content in response.content:
            if content.type == "tool_use":
                name = content.name
                assert name in self.tools, f"Tool {name} not found"
                id = content.id
                input = content.input
                assistant_message.append(
                    {
                        "type": "tool_use",
                        "id": id,
                        "name": name,
                        "input": input,
                    }
                )
        assert assistant_message, "No tool_use in response"
        self.add_assistant_message(assistant_message)

        # Extract the tool call data
        user_message = []
        for tool_use in assistant_message:
            tool = self.tools[tool_use["name"]]
            content = tool.run(**tool_use["input"])
            user_message.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use["id"],
                    "content": content,
                }
            )
        self.add_user_message(user_message)

    def paused(self):
        return any(
            message["type"] == "tool_use" and message["name"] == "wait_for_feedback"
            for message in self.conversation[-2]["content"]
        )
