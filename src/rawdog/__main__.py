import argparse
import readline

from rawdog import __version__
from rawdog.config import add_config_flags_to_argparser, get_config
from rawdog.execute_script import execute_script
from rawdog.llm_client import LLMClient
from rawdog.utils import history_file


def rawdog(prompt: str, config, llm_client):
    leash = config.get("leash")
    retries = int(config.get("retries"))
    _continue = True
    _first = True
    while _continue is True:
        error, script, output, return_code = "", "", "", 0
        try:
            if _first:
                message, script = llm_client.get_script(prompt, stream=leash)
                _first = False
            else:
                message, script = llm_client.get_script(stream=leash)
            if script:
                if leash:
                    print(f"\n{80 * '-'}")
                    if (
                        input("Execute script in markdown block? (Y/n): ")
                        .strip()
                        .lower()
                        == "n"
                    ):
                        llm_client.add_message("user", "User chose not to run script")
                        break
                output, error, return_code = execute_script(script, llm_client)
            elif message:
                print(message)
        except KeyboardInterrupt:
            break

        _continue = (output and output.strip().endswith("CONTINUE")) or (
            return_code != 0 and error and retries > 0
        )
        if error:
            retries -= 1
            llm_client.add_message("user", f"Error: {error}")
            print(f"Error: {error}")
            if script and not leash:
                print(f"{80 * '-'}\n{script}\n{80 * '-'}")
        if output:
            llm_client.add_message("user", f"LAST SCRIPT OUTPUT:\n{output}")
            if leash or not _continue:
                print(output)


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
