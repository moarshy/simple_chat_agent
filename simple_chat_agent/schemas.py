from pydantic import BaseModel

class InputSchema(BaseModel):
    messages: list
    llm_backend: str = "ollama"
