import argparse
import readline
from typing import Any

from rawdog import __version__
from rawdog.config import add_config_flags_to_argparser, get_config
from rawdog.llm_client import LLMClient
from rawdog.utils import history_file


def rawdog(prompt: str, config: dict[str, Any], llm_client: LLMClient):
    llm_client.add_user_message(prompt)
    while True:
        try:
            # TODO: implement retries
            llm_client.step()
            if llm_client.paused():
                break
        except KeyboardInterrupt:
            break


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
    parser = argparse.ArgumentParser(description=("A smart assistant that can use your computer to help or hurt you."))
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
        prompt = " ".join(args.prompt)
        rawdog(prompt, config, llm_client)
    else:
        banner(config)
        print("")
        print("What can I do for you? (Ctrl-C to exit)")
        while True:
            try:
                prompt = input("> ")
                readline.write_history_file(history_file)
                rawdog(prompt, config, llm_client)
                print("")
            except KeyboardInterrupt:
                break
    print(f"Session cost: ${llm_client.session_cost:.6f}")


if __name__ == "__main__":
    main()
