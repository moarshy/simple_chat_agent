#!/usr/bin/env python

from simple_chat_agent.schemas import InputSchema
from simple_chat_agent.utils import get_logger
from litellm import completion
import yaml

logger = get_logger(__name__)

def run(inputs: InputSchema, *args, **kwargs):
    logger.info(f"Running with inputs {inputs.prompt}")
    cfg = kwargs["cfg"]
    logger.info(f"cfg: {cfg}")

    messages = [
        {"role": "system", "content": cfg["inputs"]["system_message"]},
        {"role": "user", "content": inputs.prompt},
    ]

    api_key = None if inputs.llm_backend == "ollama" else "EMPTY"

    response = completion(
        model=cfg["models"][inputs.llm_backend]["model"],
        messages=messages,
        temperature=cfg["models"][inputs.llm_backend]["temperature"],
        max_tokens=cfg["models"][inputs.llm_backend]["max_tokens"],
        api_base=cfg["models"][inputs.llm_backend]["api_base"],
        api_key=api_key
    )

    response = response.choices[0].message.content
    logger.info(f"Response: {response}")

    return response

if __name__ == "__main__":

    cfg_path = f"simple_chat_agent/component.yaml"
    with open(cfg_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    inputs = InputSchema(
        prompt='tell me a joke',
    )
    response = run(inputs, cfg)


