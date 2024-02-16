import platform
import re
import subprocess
import sys
import tempfile
from subprocess import DEVNULL

from rawdog.utils import rawdog_dir


# Script execution environment
def get_rawdog_python_executable():
    venv_dir = rawdog_dir / "venv"
    if platform.system() == "Windows":
        python_executable = venv_dir / "Scripts" / "python"
    else:
        python_executable = venv_dir / "bin" / "python"
    if not venv_dir.exists():
        print(f"Creating virtual environment in {venv_dir}...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            stdout=DEVNULL,
            stderr=DEVNULL,
            check=True,
        )
    return str(python_executable)


def install_pip_packages(*packages: str):
    python_executable = get_rawdog_python_executable()
    print(f"Installing {', '.join(packages)} with pip...")
    return subprocess.run(
        [python_executable, "-m", "pip", "install", *packages],
        capture_output=True,
        check=True,
    )


def execute_script(script: str, llm_client) -> tuple[str, str, int]:
    python_executable = get_rawdog_python_executable()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_script:
        tmp_script_name = tmp_script.name
        tmp_script.write(script)
        tmp_script.flush()

        retry = True
        while retry:
            retry = False
            result = subprocess.run(
                [python_executable, tmp_script_name], capture_output=True, text=True
            )
            output = result.stdout
            error = result.stderr
            return_code = result.returncode
            if error and "ModuleNotFoundError: No module named" in error:
                match = re.search(r"No module named '(\w+)'", error)
                if match:
                    module = match.group(1)
                    module_name = llm_client.get_python_package(module)
                    if (
                        input(
                            f"Rawdog wants to use {module_name}. Install to rawdog's"
                            " venv with pip? (Y/n): "
                        )
                        .strip()
                        .lower()
                        != "n"
                    ):
                        install_result = install_pip_packages(module_name)
                        if install_result.returncode == 0:
                            retry = True
                        else:
                            print("Failed to install package")
    return output, error, return_code
