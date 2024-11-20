# Simple Chat Agent

This is an agent module for a simple chat agent. You can check out other examples of agent, orchestrator and environment modules using the CLI command with the [Naptha SDK](https://github.com/NapthaAI/naptha-sdk). 

## Running the Agent Module on a Naptha Node

### Pre-Requisites 

#### Install the Naptha SDK

Install the Naptha SDK using the [instructions here](https://github.com/NapthaAI/naptha-sdk).

#### (Optional) Run your own Naptha Node

You can run your own Naptha node using the [instructions here](https://github.com/NapthaAI/node) (still private, please reach out if you'd like access).

### Run the Agent Module

Using the Naptha SDK:

```bash
naptha run agent:simple_chat_agent -p "tool_name='chat' tool_input_data='what is an ai agent?'"
```

## Running the Agent Module Locally

### Pre-Requisites 

#### Install Poetry 

From the official poetry [docs](https://python-poetry.org/docs/#installing-with-the-official-installer):

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/$(whoami)/.local/bin:$PATH"
```

### Clone and Install the Agent Module

Clone the module using:

```bash
git clone https://github.com/NapthaAI/simple_chat_agent
cd simple_chat_agent
```

You can install the module using:

```bash
poetry install
```

### Running the Module

Before deploying to a Naptha node, you should iterate on improvements with the module locally. You can run the module using:

```bash
poetry run python simple_chat_agent/run.py
```
