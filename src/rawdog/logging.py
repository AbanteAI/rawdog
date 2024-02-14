import datetime
import json
from textwrap import dedent, indent
from typing import Optional

from rawdog.parsing import parse_script
from rawdog.utils import rawdog_dir


def log_conversation(
    messages: list[dict[str, str]],
    metadata: Optional[dict] = None,
    filename: Optional[str] = None,
) -> None:
    functions = {}
    conversation = []

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    my_metadata = {
        "timestamp": timestamp,
        "log_version": 0.2,
    }
    my_metadata.update(metadata or {})
    timestamp = my_metadata["timestamp"]
    for message in messages:
        if message["role"] != "assistant":
            conversation.append(message)
        else:
            content = message["content"]
            script = parse_script(content)[1]
            function_name = f"function_{len(functions)+1}"
            functions[function_name] = script
            conversation.append({"role": "assistant", "content": function_name})

    script = f"conversation = {json.dumps(conversation, indent=4)}\n\n"
    script += f"metadata = {json.dumps(my_metadata, indent=4)}\n\n\n"
    for function_name, function in functions.items():
        script += f"def {function_name}():\n" + indent(function, "    ") + "\n\n\n"

    script += dedent(f"""\
        if __name__ == "__main__":
            function_{len(functions)}()
        """)

    if filename is None:
        script_filename = rawdog_dir / f"script_{timestamp}.py"
        with open(script_filename, "w") as script_file:
            script_file.write(script)

        latest_script_filename = rawdog_dir / "latest.py"
        with open(latest_script_filename, "w") as script_file:
            script_file.write(script)
    else:
        with open(filename, "w") as script_file:
            script_file.write(script)
