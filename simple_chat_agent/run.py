#!/usr/bin/env python
from dotenv import load_dotenv
import os
from simple_chat_agent.schemas import InputSchema
from simple_chat_agent.utils import get_logger
from litellm import completion
import yaml

load_dotenv()

logger = get_logger(__name__)

class SimpleChatAgent:

    def __init__(self, cfg: dict):
        self.cfg = cfg

    def chat(self, inputs: InputSchema):

        messages = [msg for msg in inputs.tool_input_data if msg["role"] != "system"]
        messages.insert(0, {"role": "system", "content": self.cfg["inputs"]["system_message"]})

        api_key = None if inputs.llm_backend == "ollama" else ("EMPTY" if inputs.llm_backend == "vllm" else os.getenv("OPENAI_API_KEY"))

        response = completion(
            model=self.cfg["models"][inputs.llm_backend]["model"],
            messages=messages,
            temperature=self.cfg["models"][inputs.llm_backend]["temperature"],
            max_tokens=self.cfg["models"][inputs.llm_backend]["max_tokens"],
            api_base=self.cfg["models"][inputs.llm_backend]["api_base"],
            api_key=api_key
        )

        response = response.choices[0].message.content
        logger.info(f"Response: {response}")

        messages.append({"role": "assistant", "content": response})

        return messages

def run(inputs: InputSchema, *args, **kwargs):
    logger.info(f"Running with inputs {inputs.tool_input_data}")
    cfg = kwargs["cfg"]
    logger.info(f"cfg: {cfg}")

    simple_chat_agent = SimpleChatAgent(cfg)

    method = getattr(simple_chat_agent, inputs.tool_name, None)

    return method(inputs)



if __name__ == "__main__":

    cfg_path = f"simple_chat_agent/component.yaml"
    with open(cfg_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    messages = [
        {"role": "user", "content": "tell me a joke"},
    ]

    inputs = InputSchema(
        tool_name="chat",
        tool_input_data=messages,
        llm_backend="openai"
    )
    response = run(inputs, cfg=cfg)


