from rawdog.tools.base_tool import Tool, ToolOutputText


class WaitForFeedbackTool(Tool):
    name = "wait_for_feedback"
    description = "Wait for feedback from the user"
    inputs = []

    def run(self) -> ToolOutputText:
        return ToolOutputText(text="Waiting for user feedback")
