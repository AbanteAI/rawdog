import os
import json

from anthropic import Anthropic
from anthropic.lib.streaming import BetaMessageStreamManager
from dotenv import load_dotenv

from rawdog.llm_client.base_client import LLMClient
from rawdog.tools import tools, Tool, ToolOutputText, ToolOutputImage

load_dotenv()


def _build_anthropic_tool_schema(tool: Tool) -> dict:
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


def _handle_stream_response(stream_manager: BetaMessageStreamManager) -> list[dict]:
    output = []
    streaming = False
    streamed = ""
    content_block = {}
    with stream_manager as stream:
        for chunk in stream:
            if chunk.type == "content_block_stop":
                try:
                    content_block["input"] = json.loads(content_block["input"])
                except Exception:
                    content_block["input"] = {}
                output.append(content_block)
                content_block = {}
                streaming = False
                streamed = ""

            elif chunk.type == "content_block_start":
                if chunk.content_block.type == "tool_use":
                    content_block = {
                        "type": chunk.content_block.type,
                        "id": chunk.content_block.id,
                        "name": chunk.content_block.name,
                        "input": "",
                    }
                    if chunk.content_block.name == "message_user":
                        streaming = True

                else:
                    print(chunk)

                # TODO: Tell the model to only return tool_use

            elif chunk.type == "content_block_delta":
                content_block["input"] += chunk.delta.partial_json
                if streaming:
                    partial_json = content_block["input"]
                    if not partial_json.endswith('"}'):
                        partial_json += '"}'
                    try:
                        message = json.loads(partial_json).get("message", "")
                        delta = message[len(streamed) :]
                        streamed += delta
                        if delta:
                            print(delta, end="", flush=True)
                    except Exception:
                        continue

    return output


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
        response = self.client.beta.messages.stream(
            model=self.model,
            max_tokens=1024,
            temperature=self.temperature,
            tools=[_build_anthropic_tool_schema(tool) for tool in self.tools.values()],
            system=self.system,
            messages=self.messages,
            tool_choice={"type": "any"},  # Only allow tool calls
            betas=["fine-grained-tool-streaming-2025-05-14"],
        )
        # TODO: update cost

        output = _handle_stream_response(response)
        assert output, "No tool_use in response"
        self.messages.append({"role": "assistant", "content": output})

        # Extract the tool call data
        user_message = []
        for tool_use in output:
            tool = self.tools[tool_use["name"]]
            kwargs = {**tool_use["input"]}
            if tool_use["name"] == "message_user":
                kwargs["streamed"] = True
            content = tool.run(**kwargs)
            if isinstance(content, ToolOutputText):
                user_message.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use["id"],
                        "content": content.text,
                    }
                )
            elif isinstance(content, ToolOutputImage):
                user_message.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use["id"],
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": content.type,
                                    "media_type": content.media_type,
                                    "data": content.data,
                                },
                            }
                        ],
                    }
                )
        self.add_user_message(user_message)

    def paused(self):
        return any(
            message["type"] == "tool_use" and message["name"] == "wait_for_feedback"
            for message in self.messages[-2]["content"]
        )
