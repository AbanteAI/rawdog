from rawdog.tools.base_tool import Tool


class WaitForFeedbackTool(Tool):
    name = "wait_for_feedback"
    description = "Wait for feedback from the user"
    inputs = []

    def run(self) -> None:
        return "Waiting for user feedback"
