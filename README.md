# Rawdog

An CLI assistant that responds by generating and auto-executing a Python script. 

https://github.com/AbanteAI/rawdog/assets/50287275/1417a927-58c1-424f-90a8-e8e63875dcda

You'll be surprised how useful this can be:
- "How many folders in my home directory are git repos?" ... "Plot them by disk size."
- "Give me the pd.describe() for all the csv's in this directory"
- "What ports are currently active?" ... "What are the Google ones?" ... "Cancel those please."

Rawdog can self-select context by running scripts to print things, adding the output to the conversation, and then calling itself again. This works for tasks like:
- "Setup the repo per the instructions in the README"
- "Look at all these csv's and tell me if they can be merged or not, and why."
- "Try that again."

Please proceed with caution. This obviously has the potential to cause harm if so instructed.

### Quickstart
1. Install rawdog with pip:
    ```
    pip install rawdog-ai litellm
    ```

2. Choose a mode of interaction. You will be prompted to input an API key if not found:

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
* `--dry-run`: Print and manually approve each script before executing.

## Model selection
Rawdog uses `litellm` for completions with 'gpt-4' as the default. You can adjust the model or
point it to other providers by modifying `~/.rawdog/config.yaml`.
