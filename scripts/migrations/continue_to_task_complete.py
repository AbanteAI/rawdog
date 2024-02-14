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
                hasattr(module, "conversation")
            ):
                conversation = module.conversation
                for message in conversation:
                    if message["role"] == "user":
                        message["content"] = message["content"].replace(
                            "CONTINUE\n", ""
                        )
                    if message["role"] == "assistant":
                        function_name = message["content"]
                        function = getattr(module, function_name)
                        function_source = inspect.getsource(function).split("\n", 1)[1]
                        message["content"] = "```\n" + dedent(function_source)
                        if "CONTINUE" in message["content"]:
                            message["content"] = message["content"].replace(
                                'print("CONTINUE")\n', ""
                            )
                            message["content"] += '```'
                        else:
                            message["content"] += '\nprint("TASK COMPLETE")\n```'
                conversation = [{"role": "system", "content": script_prompt},
                                {"role": "system", "content": script_examples},
                                ] + conversation[2:]
                data = {"messages": conversation}
                metadata = module.metadata

                log_conversation(conversation, metadata, path)
        except Exception as e:
            print(f"Failed to migrate {path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Switch data from CONTINUE to TASK COMPLETE style.")
    parser.add_argument("dir", type=str, default=None, help="Directory to migrate")
    args = parser.parse_args()
    migrate(args.dir)
