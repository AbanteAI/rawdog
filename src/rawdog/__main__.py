import argparse
import readline

from rawdog import __version__
from rawdog.config import add_config_flags_to_argparser, get_config
from rawdog.execute_script import execute_script
from rawdog.llm_client import LLMClient
from rawdog.utils import history_file


def rawdog(prompt: str, config, llm_client):
    llm_client.add_message("user", prompt)
    leash = config.get("leash")
    retries = int(config.get("retries"))
    _continue = True
    while _continue is True:
        _continue = False
        error, script, output, return_code = "", "", "", 0
        try:
            if leash:
                print(80 * "-")
            message, script = llm_client.get_script()
            if script:
                if leash:
                    _ok = input(
                        f"\n{38 * '-'} Execute script in markdown block? (Y/n):"
                    )
                    if _ok.strip().lower() == "n":
                        llm_client.add_message("user", "User chose not to run script")
                        break
                output, error, return_code = execute_script(script, llm_client)
            elif not leash and message:
                print(message)
        except KeyboardInterrupt:
            break

        if output:
            llm_client.add_message("user", f"LAST SCRIPT OUTPUT:\n{output}")
            if output.endswith("CONTINUE"):
                _continue = True
        if error:
            llm_client.add_message("user", f"Error: {error}")
        if return_code != 0:
            retries -= 1
            if retries > 0:
                print("Retrying...\n")
                _continue = True


def banner(config):
    if config.get("leash"):
        print(f"""\
        / \__
_      (    @\___   ┳┓┏┓┏ ┓┳┓┏┓┏┓
  \    /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
   \  /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
    \/\/\/\/   U    Rawdog v{__version__}
          OO""")
    else:
        print(f"""\
   / \__
  (    @\___   ┳┓┏┓┏ ┓┳┓┏┓┏┓
  /         O  ┣┫┣┫┃┃┃┃┃┃┃┃┓
 /   (_____/   ┛┗┛┗┗┻┛┻┛┗┛┗┛
/_____/   U    Rawdog v{__version__}""")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "A smart assistant that can execute Python code to help or hurt you."
        )
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
        banner(config)
        while True:
            try:
                print("")
                if llm_client.session_cost > 0:
                    print(f"Session cost: ${llm_client.session_cost:.4f}")
                print("What can I do for you? (Ctrl-C to exit)")
                prompt = input("> ")
                # Save history after each command to avoid losing it in case of crash
                readline.write_history_file(history_file)
                print("")
                rawdog(prompt, config, llm_client)
            except KeyboardInterrupt:
                print("Exiting...")
                break


if __name__ == "__main__":
    main()
