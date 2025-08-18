from rawdog.tools.base_tool import Tool, ToolInput, ToolOutputText, ToolOutputImage  # noqa: F401
from rawdog.tools.message_user import MessageUserTool
from rawdog.tools.view_file import ViewFileTool
from rawdog.tools.wait_for_feedback import WaitForFeedbackTool

tools = [
    MessageUserTool(),
    ViewFileTool(),
    WaitForFeedbackTool(),
]
