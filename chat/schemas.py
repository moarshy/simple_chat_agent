from pydantic import BaseModel

class InputSchema(BaseModel):
    prompt: str
    llm_backend: str = "ollama"
