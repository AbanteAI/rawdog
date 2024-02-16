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
        self.data = data["date"]
        self.cwd = data["cwd"]
        self.os = data["os"]
        self.is_git = data["is_git"]
        self.cwd_info = data["cwd_info"]
        self.last_commit = data["last_commit"]
        self.retries = data["retries"]

    def _set_from_env(self):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cwd = Path.cwd()
        self.os = platform.system()
        self.is_git = "IS" if Path(".git").exists() else "is NOT"
        self.cwd_info = self._get_cwd_info()
        self.last_commit = (
            ""
            if not self.is_git
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

    def _get_cwd_info(self, max_items=100):
        output = []
        for i, item in enumerate(self.cwd.iterdir()):
            if i >= max_items:
                break
            name = ("" if not item.is_dir() else "/") + item.name
            last_modified = datetime.datetime.fromtimestamp(
                item.stat().st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")
            size, unit = 0, ""
            try:
                size = (
                    len(list(item.iterdir())) if item.is_dir() else item.stat().st_size
                )
                unit = " bytes" if item.is_file() else " items"
            except Exception:
                pass
            output.append(f"{last_modified} {size:10}{unit} {name}")
        if not output:
            return "The directory is empty."
        return "\n".join(output)

    def render_prompt(self):
        return """\
Today's date is {date}.
The current working directory is {cwd}, which {is_git} a git repository.
The user's operating system is {os}.
The contents of the current working directory are:
{cwd_info}{last_commit}{retries}""".format(
            date=self.date,
            cwd=self.cwd,
            is_git=self.is_git,
            os=self.os,
            cwd_info=self.cwd_info,
            last_commit=self.last_commit,
            retries=self.retries,
        )
