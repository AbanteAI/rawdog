import subprocess
import sys
import tempfile


def execute_script(script: str, python_executable: str = None) -> str:
    if python_executable is None:
        python_executable = sys.executable
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_script:
        tmp_script_name = tmp_script.name
        tmp_script.write(script)
        tmp_script.flush()
        result = subprocess.run([python_executable, tmp_script_name], capture_output=True, text=True)
        output = result.stdout
    return output
