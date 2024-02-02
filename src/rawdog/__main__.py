import argparse
import io

from contextlib import redirect_stdout

from rawdog.llm_client import LLMClient


llm_client = LLMClient()  # Will prompt for API key if not found


def rawdog(prompt: str, verbose: bool=False):
    _continue = True
    while _continue is True:
        error, output = "", ""
        try:
            error, script = llm_client.get_script(prompt)
            if script:
                if verbose:
                    if input("Proceed with execution? (Y/n):").strip().lower() == "n":
                        print("Execution cancelled by user.")
                        return
                with io.StringIO() as buf, redirect_stdout(buf):
                    exec(script, globals())
                    output = buf.getvalue()
        except (Exception, KeyboardInterrupt) as e:
            error = str(e)

        _continue = output and output.strip().endswith("CONTINUE")
        if error:
            print(f"Error: {error}")
            if script and not verbose:
                print(f"{80 * '-'}{script}{80 * '-'}")
        if output:
            llm_client.conversation.append(
                {"role": "user", "content": f"LAST SCRIPT OUTPUT:\n{output}"}
            )
            if verbose or not _continue:
                print(output)


def banner():
    print("""   / \__
  (    @\___   ┳┓┏┓┏ ┓┳┓┏┓┏┓
  /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
 /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
/_____/   U    Rawdog v0.1.0""")


def main():
    parser = argparse.ArgumentParser(description='A smart assistant that can execute Python code to help or hurt you.')
    parser.add_argument('prompt', nargs='*', help='Prompt for direct execution. If empty, enter conversation mode')
    parser.add_argument('--dry-run', action='store_true', help='Print the script before executing and prompt for confirmation.')
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
                rawdog(prompt, verbose=args.dry_run)
            except KeyboardInterrupt:
                print("Exiting...")
                break
