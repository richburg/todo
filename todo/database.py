import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Optional

from .models import Task
from .utilities import die


class Database:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self.file: Path = Path("~/.todo.json").expanduser()
        if not self.file.exists():
            self.file.write_text("[]")

    def get(self, id: int) -> Optional[Task]:
        """Get a task by its ID"""
        return next((task for task in self.tasks if task.id == id), None)

    def _load(self) -> None:
        try:
            with open(self.file, "r") as f:
                unparsed_tasks: list[Dict] = json.load(f)
                self.tasks = [Task(**task) for task in unparsed_tasks]
        except (json.JSONDecodeError, FileNotFoundError):
            die("Datafile is missing or corrupted")

    def _save(self) -> None:
        try:
            with open(self.file, "w") as f:
                unparsed_tasks: list[Dict] = [asdict(task) for task in self.tasks]
                json.dump(unparsed_tasks, f, indent=4)
        except FileNotFoundError:
            die("Datafile is missing")

    def __enter__(self):
        self._load()
        return self.tasks

    def __exit__(self, _, _1, _2):
        self._save()
