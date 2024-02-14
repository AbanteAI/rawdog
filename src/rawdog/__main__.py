import argparse
import os
import platform
import readline

import history_file

from rawdog import __version__
from rawdog.config import add_config_flags_to_argparser, get_config
from rawdog.execute_script import execute_script
from rawdog.llm_client import LLMClient


def rawdog(prompt: str, config, llm_client):
    verbose = config.get("dry_run")
    _continue = True
    _first = True
    while _continue is True:
        error, script, output = "", "", ""
        try:
            if _first:
                message, script = llm_client.get_script(prompt, stream=verbose)
                _first = False
            else:
                message, script = llm_client.get_script(stream=verbose)
            if script:
                if verbose:
                    print(f"{80 * '-'}")
                    if (
                        input("Execute script in markdown block? (Y/n): ")
                        .strip()
                        .lower()
                        == "n"
                    ):
                        raise Exception("Execution cancelled by user")
                output, error = execute_script(script)
            elif message:
                print(message)
        except KeyboardInterrupt:
            error = "Execution interrupted by user"

        _continue = output and output.strip().endswith("CONTINUE")
        if error:
            llm_client.conversation.append(
                {"role": "user", "content": f"Error: {error}"}
            )
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
    print(
        f"""   / \__
  (    @\___   ┳┓┏┓┏ ┓┳┓┏┓┏┓
  /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
 /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
/_____/   U    Rawdog v{__version__}"""
    )


def main():
    parser = argparse.ArgumentParser(
        description="A smart assistant that can execute Python code to help or hurt you."
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt for direct execution. If empty, enter conversation mode",
    )
    add_config_flags_to_argparser(parser)
    args = parser.parse_args()
    config = get_config(args)
    llm_client = LLMClient(config)

    if history_file.exists():
        readline.read_history_file(history_file)
    readline.set_history_length(1000)

    if len(args.prompt) > 0:
        rawdog(" ".join(args.prompt), config, llm_client)
    else:
        banner()
        while True:
            try:
                print("")
                if llm_client.session_cost > 0:
                    print(f"Session cost: ${llm_client.session_cost:.4f}")
                print("What can I do for you? (Ctrl-C to exit)")
                prompt = input(f"> ")
                # Save history after each command to avoid losing it in case of crash
                readline.write_history_file(history_file)
                print("")
                rawdog(prompt, config, llm_client)
            except KeyboardInterrupt:
                print("Exiting...")
                break


if __name__ == "__main__":
    main()
