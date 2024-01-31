# Rawdog

A command-line utility that just generates and auto-executes Python scripts.

You'll be surprised how useful it can be:
- "How many folders in my home directory are git repos?" ... "Plot them by disk size."
- "Give me the pd.describe() for all the csv's in this directory"
- "What ports are currently active?" ... "What are the Google ones?" ... "Cancel those please."

Please proceed with caution. This obviously has the potential to cause harm if so instructed.

### Quickstart
1. Clone the repo: 
    ```
    git clone http://github.com/AbanteAI/rawdog
    cd rawdog
    ```
2. Install it locally with pip
    ```
    pip install -e .
    ```

3. Choose a mode of interaction. You will be prompted to input your API key if not found:

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
* `--continuation`: Let the model run scripts to generate context for itself before completing the task.

## Model selection
Rawdog uses `litellm` for completions with 'gpt-4' as the default. You can adjust the model or
point it to other providers by modifying `~/.rawdog/config.yaml`.
