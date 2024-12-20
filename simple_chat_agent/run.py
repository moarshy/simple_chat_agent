#!/usr/bin/env python
import logging
from dotenv import load_dotenv
import json
from litellm import completion
from naptha_sdk.schemas import AgentDeployment, AgentRunInput
import os
from simple_chat_agent.schemas import InputSchema, SystemPromptSchema

load_dotenv()

logger = logging.getLogger(__name__)

class SimpleChatAgent:

    def __init__(self, agent_deployment: AgentDeployment):
        self.agent_deployment = agent_deployment
        self.system_prompt = SystemPromptSchema(role=agent_deployment.agent_config.system_prompt["role"], persona=agent_deployment.agent_config.persona_module["data"])

    def chat(self, inputs: InputSchema):
        if isinstance(inputs.tool_input_data, list):
            messages = [msg for msg in inputs.tool_input_data if msg["role"] != "system"]
        elif isinstance(inputs.tool_input_data, str):
            messages = [{"role": "user", "content": inputs.tool_input_data}]
        messages.insert(0, {"role": "system", "content": json.dumps(self.agent_deployment.agent_config.system_prompt)})

        api_key = None if self.agent_deployment.agent_config.llm_config.client == "ollama" else ("EMPTY" if self.agent_deployment.agent_config.llm_config.client == "vllm" else os.getenv("OPENAI_API_KEY"))

        response = completion(
            model=self.agent_deployment.agent_config.llm_config.model,
            messages=messages,
            temperature=self.agent_deployment.agent_config.llm_config.temperature,
            max_tokens=self.agent_deployment.agent_config.llm_config.max_tokens,
            api_base=self.agent_deployment.agent_config.llm_config.api_base,
            api_key=api_key
        )

        response = response.choices[0].message.content
        logger.info(f"Response: {response}")

        messages.append({"role": "assistant", "content": response})

        return messages

def run(agent_run: AgentRunInput, *args, **kwargs):
    logger.info(f"Running with inputs {agent_run.inputs.tool_input_data}")

    simple_chat_agent = SimpleChatAgent(agent_run.agent_deployment)

    method = getattr(simple_chat_agent, agent_run.inputs.tool_name, None)

    return method(agent_run.inputs)


if __name__ == "__main__":
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import load_agent_deployments

    naptha = Naptha()

    # Configs
    agent_deployments = load_agent_deployments("simple_chat_agent/configs/agent_deployments.json")

    input_params = InputSchema(
        tool_name="chat",
        tool_input_data=[{"role": "user", "content": "tell me a joke"}],
    )

    agent_run = AgentRunInput(
        inputs=input_params,
        agent_deployment=agent_deployments[0],
        consumer_id=naptha.user.id,
    )

    response = run(agent_run)


