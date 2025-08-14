from pathlib import Path
import base64
import mimetypes

from rawdog.tools.base_tool import Tool, ToolInput, ToolOutputText, ToolOutputImage


class ViewFileTool(Tool):
    name = "view_file"
    description = "View a text or image file"
    inputs = [
        ToolInput(
            name="file_path",
            type="string",
            description="The path to the file to view. Support text and image files.",
            required=True,
        ),
        ToolInput(
            name="start_line",
            type="integer",
            description="The line number to start viewing from",
            required=False,
        ),
        ToolInput(
            name="end_line",
            type="integer",
            description="The line number to end viewing at",
            required=False,
        ),
    ]

    def run(self, file_path: str, start_line: int = None, end_line: int = None) -> ToolOutputText | ToolOutputImage:
        if not Path(file_path).exists():
            return ToolOutputText(text=f"File not found: {file_path}")
        print(f"Viewing file: {file_path}...")

        try:
            mime_type = mimetypes.guess_type(file_path)[0]
            if mime_type.startswith("image/"):
                data = base64.b64encode(Path(file_path).read_bytes()).decode("utf-8")
                return ToolOutputImage(type="base64", media_type=mime_type, data=data)

            if mime_type.startswith("text/"):
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    if start_line:
                        lines = lines[start_line:]
                    if end_line:
                        lines = lines[:end_line]
                    return ToolOutputText(text="\n".join(lines))

            return ToolOutputText(text=f"Unsupported file type: {mime_type}")
        except Exception as e:
            return ToolOutputText(text=f"Error reading file: {e}")
