[![Discord Follow](https://dcbadge.vercel.app/api/server/XbPdxAMJte?style=flat)](https://discord.gg/zbvd9qx9Pb)

# Rawdog

An CLI assistant that responds by generating and auto-executing a Python script. 

https://github.com/AbanteAI/rawdog/assets/50287275/1417a927-58c1-424f-90a8-e8e63875dcda

You'll be surprised how useful this can be:
- "How many folders in my home directory are git repos?" ... "Plot them by disk size."
- "Give me the pd.describe() for all the csv's in this directory"
- "What ports are currently active?" ... "What are the Google ones?" ... "Cancel those please."

Rawdog (Recursive Augmentation With Deterministic Output Generations) is a novel alternative to RAG
(Retrieval Augmented Generation). Rawdog can self-select context by running scripts to print things,
adding the output to the conversation, and then calling itself again. 

This works for tasks like:
- "Setup the repo per the instructions in the README"
- "Look at all these csv's and tell me if they can be merged or not, and why."
- "Try that again."

Please proceed with caution. This obviously has the potential to cause harm if so instructed.

### Quickstart
1. Install rawdog with pip:
    ```
    pip install rawdog-ai
    ```

2. Export your api key. See [Model selection](#model-selection) for how to use other providers

    ```
    export OPENAI_API_KEY=your-api-key
    ```

3. Choose a mode of interaction.

    Direct: Execute a single prompt and close
    ```
    rawdog Plot the size of all the files and directories in cwd
    ```
    
    Conversation: Initiate back-and-forth until you close. Rawdog can see its scripts and output.
    ```
    rawdog
    >>> What can I do for you? (Ctrl-C to exit)
    >>> > |
    ```

## Optional Arguments
* `--leash`: (default False) Print and manually approve each script before executing.
* `--retries`: (default 2) If rawdog's script throws an error, review the error and try again.

## Model selection
Rawdog uses `litellm` for completions with 'gpt-4-turbo-preview' as the default. You can adjust the model or
point it to other providers by modifying `~/.rawdog/config.yaml`. Some examples:

To use gpt-3.5 turbo a minimal config is:
```yaml
llm_model: gpt-3.5-turbo
```

To run mixtral locally with ollama a minimal config is (assuming you have [ollama](https://ollama.ai/)
installed and a sufficient gpu):
```yaml
llm_custom_provider: ollama
llm_model: mixtral
```

To run claude-2.1 set your API key:
```bash
export ANTHROPIC_API_KEY=your-api-key
```
and then set your config:
```yaml
llm_model: claude-2.1
```

If you have a model running at a local endpoint (or want to change the baseurl for some other reason)
you can set the `llm_base_url`. For instance if you have an openai compatible endpoint running at
http://localhost:8000 you can set your config to:
```
llm_base_url: http://localhost:8000
llm_model: openai/model # So litellm knows it's an openai compatible endpoint
```

Litellm supports a huge number of providers including Azure, VertexAi and Huggingface. See
[their docs](https://docs.litellm.ai/docs/) for details on what environment variables, model names
and llm_custom_providers you need to use for other providers.
