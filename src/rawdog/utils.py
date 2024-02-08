import datetime
import platform
from pathlib import Path

import yaml

# Rawdog dir
rawdog_dir = Path.home() / ".rawdog"
rawdog_dir.mkdir(exist_ok=True)

# Command history file
history_file = rawdog_dir / "cmdline_history"

# Config
config_path = rawdog_dir / "config.yaml"


class EnvInfo:
    def __init__(self, data=None):
        if data:
            self._set_from_dict(data)
        else:
            self._set_from_env()

    def _set_from_dict(self, data):
        """Used when preparing fine-tuning examples"""
        self.data = data["date"]
        self.cwd = data["cwd"]
        self.os = data["os"]
        self.is_git = data["is_git"]

    def _set_from_env(self):
        self.date = datetime.date.today().isoformat()
        self.cwd = Path.cwd()
        self.os = platform.system()
        self.is_git = "IS" if Path(".git").exists() else "is NOT"

    def render_prompt(self):
        return """\
Today's date is {date}.
The current working directory is {cwd}, which {is_git} a git repository.
The user's operating system is {os}
        """.format(
            date=self.date, cwd=self.cwd, is_git=self.is_git, os=self.os
        )


def load_config():
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    else:
        return {}


def save_config(config):
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)


# Config helpers
def get_llm_base_url():
    config = load_config()
    return config.get("llm_base_url")


def get_llm_model():
    config = load_config()
    return config.get("llm_model")


def get_llm_custom_provider():
    config = load_config()
    return config.get("llm_custom_provider")


def set_llm_model(model_name: str):
    config = load_config()
    config["llm_model"] = model_name
    save_config(config)


def set_base_url(base_url: str):
    config = load_config()
    config["llm_base_url"] = base_url
    save_config(config)


def set_llm_custom_provider(custom_provider: str):
    config = load_config()
    config["llm_custom_provider"] = custom_provider
    save_config(config)
