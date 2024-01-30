import argparse
import io

from contextlib import redirect_stdout

from rawdog.llm_client import LLMClient


def rawdog(prompt: str):
    output = None
    error, script = llm_client.get_script(prompt)
    if script:
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                exec(script, globals())
                output = buf.getvalue()
            print(output)
        except Exception as e:
            error = f"Executing the script raised an Exception: {e}"
    if error:
        print(f"Error: {error}")
        if script:
            print(f"{80 * '-'}{script}{80 * '-'}")
    return output


def banner():
    print("""   / \__
  (    @\___   ┳┓┏┓┓ ┏┳┓┏┓┏┓
  /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
 /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
/_____/   U    Rawdog v0.1.0""")


# Main Loop
parser = argparse.ArgumentParser(description='A smart assistant that can execute Python code to help or hurt you.')
parser.add_argument('prompt', nargs='*', help='Prompt for direct execution. If empty, enter conversation mode')
args = parser.parse_args()
llm_client = LLMClient()  # Will prompt for API key if not found
if len(args.prompt) > 0:
    rawdog(" ".join(args.prompt))
else:
    banner()
    while True:
        try:
            print("\nWhat can I do for you? (Ctrl-C to exit)")
            prompt = input("> ")
            print("")
            output = rawdog(prompt)
            llm_client.conversation.append({"role": "system", "content": f"LAST SCRIPT OUTPUT:\n{output}"})
        except KeyboardInterrupt:
            print("Exiting...")
            break
