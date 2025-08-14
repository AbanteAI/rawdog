from pydantic import BaseModel


class ToolInput(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True


class ToolOutput(BaseModel):
    pass


class ToolOutputText(ToolOutput):
    text: str


class ToolOutputImage(ToolOutput):
    type: str
    media_type: str
    data: str


class Tool:
    name: str
    description: str
    inputs: list[ToolInput]

    def run(self, *args, **kwargs) -> ToolOutput:
        raise NotImplementedError
