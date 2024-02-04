import argparse
import io

from contextlib import redirect_stdout

from rawdog.llm_client import LLMClient


llm_client = LLMClient()  # Will prompt for API key if not found


def rawdog(prompt: str, verbose: bool=False, temperature: float=1.0):
    _continue = True
    while _continue is True:
        error, script, output = "", "", ""
        try:
            message, script = llm_client.get_script(prompt, temperature)
            if script:
                if verbose:
                    _message = f"{message}\n" if message else ""
                    print(f"{80 * '-'}\n{_message}{script}\n{80 * '-'}")
                    if input("Proceed with execution? (Y/n):").strip().lower() == "n":
                        raise Exception("Execution cancelled by user")
                with io.StringIO() as buf, redirect_stdout(buf):
                    exec(script, globals())
                    output = buf.getvalue()
            elif message:
                print(message)
        except KeyboardInterrupt:
            error = "Execution interrupted by user"
        except Exception as e:
            error = f"Execution error: {e}"

        _continue = output and output.strip().endswith("CONTINUE")
        if error:
            llm_client.conversation.append(
                {"role": "system", "content": f"Error: {error}"}
            )
            print(f"Error: {error}")
            if script and not verbose:
                print(f"{80 * '-'}{script}{80 * '-'}")
        if output:
            llm_client.conversation.append(
                {"role": "assistant", "content": f"LAST SCRIPT OUTPUT:\n{output}"}
            )
            if verbose or not _continue:
                print(output)
        if _continue:
            llm_client.conversation.append(
                {"role": "user", "content": prompt}
            )


def banner():
    print("""   / \__
  (    @\___   ┳┓┏┓┏ ┓┳┓┏┓┏┓
  /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
 /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
/_____/   U    Rawdog v0.1.1""")


def main():
    parser = argparse.ArgumentParser(description='A smart assistant that can execute Python code to help or hurt you.')
    parser.add_argument('prompt', nargs='*', help='Prompt for direct execution. If empty, enter conversation mode')
    parser.add_argument('--dry-run', action='store_true', help='Print the script before executing and prompt for confirmation.')
    parser.add_argument('--temperature', type=float, default=1.0, help='The temperature of the language model (default: 1.)')
    args = parser.parse_args()

    if len(args.prompt) > 0:
        rawdog(" ".join(args.prompt))
    else:
        banner()
        while True:
            try:
                print("\nWhat can I do for you? (Ctrl-C to exit)")
                prompt = input("> ")
                print("")
                rawdog(prompt, verbose=args.dry_run, temperature=args.temperature)
            except KeyboardInterrupt:
                print("Exiting...")
                break
