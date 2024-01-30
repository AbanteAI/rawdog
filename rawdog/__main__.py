import argparse

from rawdog.llm_client import LLMClient


def rawdog(prompt: str):
    error, script = llm_client.get_script(prompt)
    if script:
        try:
            exec(script, globals())
        except Exception as e:
            error = f"Executing the script raised an Exception: {e}"
    if error:
        print(f"Error: {error}")
        if script:
            print(f"{80 * '-'}{script}{80 * '-'}")


# Main Loop
parser = argparse.ArgumentParser(description='A smart assistant for processing email data.')
parser.add_argument('prompt', nargs='*', help='Prompt for direct execution. If empty, enter conversation mode')
args = parser.parse_args()
llm_client = LLMClient()  # Will prompt for API key if not found
if len(args.prompt) > 0:
    rawdog(" ".join(args.prompt))
else:
    while True:
        try:
            print("\nWhat can I do for you? (Ctrl-C to exit)")
            prompt = input("> ")
            print("")
            rawdog(prompt)
        except KeyboardInterrupt:
            print("Exiting...")
            break
