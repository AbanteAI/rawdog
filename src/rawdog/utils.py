import datetime
import platform
from pathlib import Path

# Rawdog dir
rawdog_dir = Path.home() / ".rawdog"
rawdog_log_path = rawdog_dir / "logs.jsonl"
rawdog_dir.mkdir(exist_ok=True)

# Command history file
history_file = rawdog_dir / "cmdline_history"


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
