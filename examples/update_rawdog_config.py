# PROMPT INFORMATION
conversation = [
    {
        "role": "user",
        "content": "PROMPT: Can you read the readme and use the information to change rawdog to use mixtral with ollama?"
    },
    {
        "role": "system",
        "content": "SCRIPT: \n```\nwith open(\"README.md\", \"r\") as f:\n    guide_contents = f.read()\nprint(guide_contents)\nprint(\"CONTINUE\")\n```"
    },
    {
        "role": "assistant",
        "content": "LAST SCRIPT OUTPUT:\n[![Discord Follow](https://dcbadge.vercel.app/api/server/XbPdxAMJte?style=flat)](https://discord.gg/zbvd9qx9Pb)\n\n# Rawdog\n\nAn CLI assistant that responds by generating and auto-executing a Python script. \n\nhttps://github.com/AbanteAI/rawdog/assets/50287275/1417a927-58c1-424f-90a8-e8e63875dcda\n\nYou'll be surprised how useful this can be:\n- \"How many folders in my home directory are git repos?\" ... \"Plot them by disk size.\"\n- \"Give me the pd.describe() for all the csv's in this directory\"\n- \"What ports are currently active?\" ... \"What are the Google ones?\" ... \"Cancel those please.\"\n\nRawdog (Recursive Augmentation With Deterministic Output Generations) is a novel alternative to RAG\n(Retrieval Augmented Generation). Rawdog can self-select context by running scripts to print things,\nadding the output to the conversation, and then calling itself again. \n\nThis works for tasks like:\n- \"Setup the repo per the instructions in the README\"\n- \"Look at all these csv's and tell me if they can be merged or not, and why.\"\n- \"Try that again.\"\n\nPlease proceed with caution. This obviously has the potential to cause harm if so instructed.\n\n### Quickstart\n1. Install rawdog with pip:\n    ```\n    pip install rawdog-ai\n    ```\n\n2. Export your api key. See [Model selection](#model-selection) for how to use other providers\n\n    ```\n    export OPENAI_API_KEY=your-api-key\n    ```\n\n3. Choose a mode of interaction.\n\n    Direct: Execute a single prompt and close\n    ```\n    rawdog Plot the size of all the files and directories in cwd\n    ```\n    \n    Conversation: Initiate back-and-forth until you close. Rawdog can see its scripts and output.\n    ```\n    rawdog\n    >>> What can I do for you? (Ctrl-C to exit)\n    >>> > |\n    ```\n\n## Optional Arguments\n* `--dry-run`: Print and manually approve each script before executing.\n\n## Model selection\nRawdog uses `litellm` for completions with 'gpt-4' as the default. You can adjust the model or\npoint it to other providers by modifying `~/.rawdog/config.yaml`. Some examples:\n\nTo use gpt-3.5 turbo a minimal config is:\n```yaml\nllm_model: gpt-3.5-turbo\n```\n\nTo run mixtral locally with ollama a minimal config is (assuming you have [ollama](https://ollama.ai/)\ninstalled and a sufficient gpu):\n```yaml\nllm_custom_provider: ollama\nllm_model: mixtral\n```\n\nTo run claude-2.1 set your API key:\n```bash\nexport ANTHROPIC_API_KEY=your-api-key\n```\nand then set your config:\n```yaml\nllm_model: claude-2.1\n```\n\nIf you have a model running at a local endpoint (or want to change the baseurl for some other reason)\nyou can set the `llm_base_url`. For instance if you have an openai compatible endpoint running at\nhttp://localhost:8000 you can set your config to:\n```\nllm_base_url: http://localhost:8000\nllm_model: openai/model # So litellm knows it's an openai compatible endpoint\n```\n\nLitellm supports a huge number of providers including Azure, VertexAi and Huggingface. See\n[their docs](https://docs.litellm.ai/docs/) for details on what environment variables, model names\nand llm_custom_providers you need to use for other providers.\n\nCONTINUE\n"
    },
    {
        "role": "user",
        "content": "Can you read the readme and use the information to change rawdog to use mixtral with ollama?"
    },
    {
        "role": "user",
        "content": "PROMPT: Can you read the readme and use the information to change rawdog to use mixtral with ollama?"
    }
]
metadata = {
    "model": "gpt-4",
    "cost": "0.0686700000",
    "timestamp": "2024-02-06_13-53-18"
}
# START SCRIPT
import os
import yaml

# Check if config file exists. If not, create one
config_path = os.path.expanduser("~/.rawdog/config.yaml")
if not os.path.exists(config_path):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as config_file:
        config_file.write("")

# Load the existing config
with open(config_path, 'r') as config_file:
    config_data = yaml.safe_load(config_file)

# Modify the model and custom provider
config_data['llm_model'] = 'mixtral'
config_data['llm_custom_provider'] = 'ollama'

# Write back the config
with open(config_path, 'w') as config_file:
    yaml.safe_dump(config_data, config_file)

print("Successfully changed the configuration to use mixtral with ollama.")