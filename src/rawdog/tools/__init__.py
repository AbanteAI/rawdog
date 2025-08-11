from rawdog.tools.base_tool import Tool, ToolInput  # noqa: F401
from rawdog.tools.message_user import MessageUserTool
from rawdog.tools.wait_for_feedback import WaitForFeedbackTool

tools = [
    MessageUserTool(),
    WaitForFeedbackTool(),
]
