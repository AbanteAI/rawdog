conversation = [
    {
        "role": "system",
        "content": "You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.\n\nA typical interaction goes like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n3. The compiler checks your SCRIPT using ast.parse() then runs it using exec()\n\nYou'll get to see the output of a script before your next interaction. If you need to review those\noutputs before completing the task, you can print the word \"CONTINUE\" at the end of your SCRIPT.\nThis can be useful for summarizing documents or technical readouts, reading instructions before\ndeciding what to do, or other tasks that require multi-step reasoning.\nA typical 'CONTINUE' interaction looks like this:\n1. The user gives you a natural language PROMPT.\n2. You:\n    i. Determine what needs to be done\n    ii. Determine that you need to see the output of some subprocess call to complete the task\n    iii. Write a short Python SCRIPT to print that and then print the word \"CONTINUE\"\n3. The compiler\n    i. Checks and runs your SCRIPT\n    ii. Captures the output and appends it to the conversation as \"LAST SCRIPT OUTPUT:\"\n    iii. Finds the word \"CONTINUE\" and sends control back to you\n4. You again:\n    i. Look at the original PROMPT + the \"LAST SCRIPT OUTPUT:\" to determine what needs to be done\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nWhen your script raises an exception, you'll get to review the error and try again:\n1. The user gives you a natural language PROMPT.\n2. You: Respond with a SCRIPT..\n3. The compiler\n    i. Executes your SCRIPT\n    ii. Catches an exception\n    iii. Adds it to the conversation\n    iv. If there are retries left, sends control back to you\n4. You again:\n    i. Look at the latest PROMPT, SCRIPT and Error message, determine what caused the error and how to fix it\n    ii. Write a short Python SCRIPT to do it\n    iii. Communicate back to the user by printing to the console in that SCRIPT\n5. The compiler...\n\nPlease follow these conventions carefully:\n- Decline any tasks that seem dangerous, irreversible, or that you don't understand.\n- Always review the full conversation prior to answering and maintain continuity.\n- If asked for information, just print the information clearly and concisely.\n- If asked to do something, print a concise summary of what you've done as confirmation.\n- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.\n- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.\n- The user will likely not specify exact filenames. Use glob searches when looking for filenames in your SCRIPT.\n- Actively clean up any temporary processes or files you use.\n- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.\n- Let exceptions propagate to the user (rather than catching them in your SCRIPT) so that you can retry.\n- At the user's request, you can inspect and update your configuration file: ~/.rawdog/config.yaml. Changes will take effect after restarting.\n- Feel free to use any common python packages. For example matplotlib, beautifulsoup4, numpy. If the user doesn't have them installed they will be installed automatically with user confirmation.\n- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.\n"
    },
    {
        "role": "system",
        "content": "EXAMPLES:\n-------------------------------------------------------------------------------\nPROMPT: Kill the process running on port 3000\n\nSCRIPT:\n```\nimport os\nos.system(\"kill $(lsof -t -i:3000)\")\nprint(\"Process killed\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Rename the photos in this directory with \"nyc\" and their timestamp\n\nSCRIPT:\n```\nimport os\nimport time\nimage_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\ndef get_name(f):\n    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(os.path.getmtime(f)))\n    return f\"nyc_{timestamp}{os.path.splitext(f)[1]}\"\n[os.rename(f, get_name(f)) for f in image_files]\nprint(\"Renamed files\")\n```\n-------------------------------------------------------------------------------\nPROMPT: Summarize my essay\n\nSCRIPT:\n```\nimport glob\nfiles = glob.glob(\"*essay*.*\")\nwith open(files[0], \"r\") as f:\n    print(f.read())\nprint(\"CONTINUE\")\n```\n\nLAST SCRIPT OUTPUT:\n\nJohn Smith\nEssay 2021-09-01\n...\n\nSCRIPT:\n```\nprint(\"The essay is about...\")\n```\n-------------------------------------------------------------------------------\n"
    },
    {
        "role": "system",
        "content": "Today's date is 2024-02-08.\nThe current working directory is /Users/jakekoenig/rawdog, which IS a git repository.\nThe user's operating system is Darwin\n        "
    },
    {
        "role": "user",
        "content": "Can you read the readme and use the information to change rawdog to use mixtral with ollama?"
    },
    {
        "role": "assistant",
        "content": "function_1"
    },
    {
        "role": "user",
        "content": "LAST SCRIPT OUTPUT:\n[![Discord Follow](https://dcbadge.vercel.app/api/server/XbPdxAMJte?style=flat)](https://discord.gg/zbvd9qx9Pb)\n\n# Rawdog\n\nAn CLI assistant that responds by generating and auto-executing a Python script. \n\nhttps://github.com/AbanteAI/rawdog/assets/50287275/1417a927-58c1-424f-90a8-e8e63875dcda\n\nYou'll be surprised how useful this can be:\n- \"How many folders in my home directory are git repos?\" ... \"Plot them by disk size.\"\n- \"Give me the pd.describe() for all the csv's in this directory\"\n- \"What ports are currently active?\" ... \"What are the Google ones?\" ... \"Cancel those please.\"\n\nRawdog (Recursive Augmentation With Deterministic Output Generations) is a novel alternative to RAG\n(Retrieval Augmented Generation). Rawdog can self-select context by running scripts to print things,\nadding the output to the conversation, and then calling itself again. \n\nThis works for tasks like:\n- \"Setup the repo per the instructions in the README\"\n- \"Look at all these csv's and tell me if they can be merged or not, and why.\"\n- \"Try that again.\"\n\nPlease proceed with caution. This obviously has the potential to cause harm if so instructed.\n\n### Quickstart\n1. Install rawdog with pip:\n    ```\n    pip install rawdog-ai\n    ```\n\n2. Export your api key. See [Model selection](#model-selection) for how to use other providers\n\n    ```\n    export OPENAI_API_KEY=your-api-key\n    ```\n\n3. Choose a mode of interaction.\n\n    Direct: Execute a single prompt and close\n    ```\n    rawdog Plot the size of all the files and directories in cwd\n    ```\n    \n    Conversation: Initiate back-and-forth until you close. Rawdog can see its scripts and output.\n    ```\n    rawdog\n    >>> What can I do for you? (Ctrl-C to exit)\n    >>> > |\n    ```\n\n## Optional Arguments\n* `--leash`: Print and manually approve each script before executing.\n\n## Model selection\nRawdog uses `litellm` for completions with 'gpt-4' as the default. You can adjust the model or\npoint it to other providers by modifying `~/.rawdog/config.yaml`. Some examples:\n\nTo use gpt-3.5 turbo a minimal config is:\n```yaml\nllm_model: gpt-3.5-turbo\n```\n\nTo run mixtral locally with ollama a minimal config is (assuming you have [ollama](https://ollama.ai/)\ninstalled and a sufficient gpu):\n```yaml\nllm_custom_provider: ollama\nllm_model: mixtral\n```\n\nTo run claude-2.1 set your API key:\n```bash\nexport ANTHROPIC_API_KEY=your-api-key\n```\nand then set your config:\n```yaml\nllm_model: claude-2.1\n```\n\nIf you have a model running at a local endpoint (or want to change the baseurl for some other reason)\nyou can set the `llm_base_url`. For instance if you have an openai compatible endpoint running at\nhttp://localhost:8000 you can set your config to:\n```\nllm_base_url: http://localhost:8000\nllm_model: openai/model # So litellm knows it's an openai compatible endpoint\n```\n\nLitellm supports a huge number of providers including Azure, VertexAi and Huggingface. See\n[their docs](https://docs.litellm.ai/docs/) for details on what environment variables, model names\nand llm_custom_providers you need to use for other providers.\n\nCONTINUE\n"
    },
    {
        "role": "assistant",
        "content": "function_2"
    }
]

metadata = {
    "timestamp": "2024-02-07_09-00-18",
    "log_version": "0.2",
    "model": "openai/gpt-4-turbo-preview",
    "cost": "0.0240200000"
}


def function_1():
    with open("README.md", "r") as f:
        content = f.read()
        print(content)
    print("CONTINUE")


def function_2():
    import os

    config_path = os.path.expanduser('~/.rawdog/config.yaml')
    config_content = '''llm_custom_provider: ollama
    llm_model: mixtral
    '''

    # Create backup before modifying
    backup_path = config_path + '.bak'
    if not os.path.exists(backup_path):
        os.system(f'cp {config_path} {backup_path}')

    # Write new configuration
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)

    print("Updated Rawdog to use Mixtral with Ollama. A backup of the previous configuration was saved as ~/.rawdog/config.yaml.bak")


if __name__ == "__main__":
    function_2()
