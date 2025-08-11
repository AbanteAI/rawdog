from pydantic import BaseModel


class ToolInput(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True


class Tool:
    name: str
    description: str
    inputs: list[ToolInput]

    def run(self, *args, **kwargs) -> str:
        raise NotImplementedError
