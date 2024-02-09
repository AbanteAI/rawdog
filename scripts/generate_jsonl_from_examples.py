import json
import os
import sys
import importlib.util
import inspect
from textwrap import dedent

def write_finetuning_data(path):
    try:
        spec = importlib.util.spec_from_file_location("", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'conversation') and hasattr(module, 'main'):
            data = module.conversation
            source = inspect.getsource(module.main).split("\n", 1)[1]
            data.append({"role": "assistant", "content": "```\n" + dedent(source) + "```"})
            with open("training_data.jsonl", "a") as f:
                json.dump(data, f)
                f.write("\n")
    except Exception as e:
        print(f"Failed to import {module_name} from {path}: {e}")

def find_python_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def make_finetuning_data_from_paths(paths):
    if not paths:
        scripts_dir = os.path.dirname(os.path.realpath(__file__))
        examples_dir = os.path.join(os.path.dirname(scripts_dir), "examples")
        paths = [examples_dir]

    for path in paths:
        if os.path.isdir(path):
            for file_path in find_python_files(path):
                write_finetuning_data(file_path)
        else:
            write_finetuning_data(path)

if __name__ == "__main__":
    make_finetuning_data_from_paths(sys.argv[1:])
