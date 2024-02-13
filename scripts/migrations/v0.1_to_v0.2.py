import argparse
import importlib.util
import inspect
import os
from textwrap import dedent

from rawdog.logging import log_conversation
from rawdog.prompts import script_examples, script_prompt


def find_python_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def migrate(directory):
    for path in find_python_files(directory):
        try:
            spec = importlib.util.spec_from_file_location("", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if (
                hasattr(module, "metadata")
                and module.metadata.get("log_version") == 0.1
            ):
                conversation = module.conversation
                main_source = inspect.getsource(module.main).split("\n", 1)[1]
                conversation.append(
                    {
                        "role": "assistant",
                        "content": "```\n" + dedent(main_source) + "```",
                    }
                )
                system_prompts = [
                    {"role": "system", "content": script_prompt},
                    {"role": "system", "content": script_examples},
                ]
                conversation = system_prompts + conversation
                metadata = module.metadata
                metadata["log_version"] = "0.2"
                log_conversation(conversation, metadata, path)
        except Exception as e:
            print(f"Failed to migrate {path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate examples from v0.1 to v0.2")
    parser.add_argument("dir", type=str, default=None, help="Directory to migrate")
    args = parser.parse_args()
    migrate(args.dir)
