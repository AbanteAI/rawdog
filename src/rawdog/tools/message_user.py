from rawdog.tools.base_tool import Tool, ToolInput


class MessageUserTool(Tool):
    name = "message_user"
    description = "Send a message to the user"
    inputs = [
        ToolInput(
            name="message",
            type="string",
            description="The message to send to the user",
            required=True,
        )
    ]

    def run(self, message: str) -> str:
        print(message)
        return "Sent message to user"
