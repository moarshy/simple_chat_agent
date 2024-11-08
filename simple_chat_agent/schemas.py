from pydantic import BaseModel

class InputSchema(BaseModel):
    tool_name: str
    tool_input_data: list
    llm_backend: str = "ollama"
