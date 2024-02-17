import datetime
import platform
import subprocess
from pathlib import Path

# Rawdog dir
rawdog_dir = Path.home() / ".rawdog"
rawdog_log_path = rawdog_dir / "logs.jsonl"
rawdog_dir.mkdir(exist_ok=True)

# Command history file
history_file = rawdog_dir / "cmdline_history"


class EnvInfo:
    def __init__(self, config=None, data=None):
        self.config = config
        if data:
            self._set_from_dict(data)
        else:
            self._set_from_env()

    def _set_from_dict(self, data):
        """Used when preparing fine-tuning examples"""
        self.date = data["date"]
        self.cwd = data["cwd"]
        self.os = data["os"]
        self.is_git = data["is_git"]
        self.last_commit = data["last_commit"]
        self.retries = data["retries"]

    def _set_from_env(self):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cwd = Path.cwd()
        self.os = platform.system()
        _is_git = Path(".git").exists()
        self.is_git = "IS" if _is_git else "is NOT"
        self.last_commit = (
            ""
            if not _is_git
            else "\nThe last commit message is: "
            + (
                subprocess.run(
                    ["git", "log", "-1", "--pretty=%B"], stdout=subprocess.PIPE
                )
                .stdout.decode()
                .strip()
            )
        )
        _retries = 0 if self.config is None else self.config.get("retries")
        self.retries = f"\nYou'll get {_retries} retries."

    def render_prompt(self):
        return """\
Today's date is {date}.
The current working directory is {cwd}, which {is_git} a git repository.
The user's operating system is {os}.{last_commit}{retries}""".format(
            date=self.date,
            cwd=self.cwd,
            is_git=self.is_git,
            os=self.os,
            last_commit=self.last_commit,
            retries=self.retries,
        )


def is_finetuned_model(model: str):
    return "rawdog" in model or "abante" in model
