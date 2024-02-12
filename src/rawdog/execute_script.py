import subprocess
import tempfile

from rawdog.utils import get_rawdog_python_executable


def execute_script(script: str) -> str:
    python_executable = get_rawdog_python_executable()
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_script:
        tmp_script_name = tmp_script.name
        tmp_script.write(script)
        tmp_script.flush()
        result = subprocess.run([python_executable, tmp_script_name], capture_output=True, text=True)
        output = result.stdout
    return output
