import json
from dataclasses import asdict, dataclass
from pathlib import Path
from todo.helpers import die, warning


@dataclass
class Task:
    id: int
    description: str
    done: bool = False


class Database:
    def __init__(self, data_file: Path):
        self.data_file = data_file

    def load_tasks(self) -> list[Task]:
        try:
            with open(self.data_file, "r") as file:
                unformatted_tasks: list[dict] = json.load(file)
                return [Task(**task) for task in unformatted_tasks]
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            die("Database file is corrupted or missing")
            return []

    def save_tasks(self, tasks: list[Task]) -> None:
        with open(self.data_file, "w") as file:
            json.dump([asdict(task) for task in tasks], file, indent=4)

    def find_task(self, task_id: int) -> tuple[Task | None, list[Task]]:
        tasks = self.load_tasks()
        task = next((task for task in tasks if task.id == task_id), None)
        if not task:
            warning(f"Unable to find task with ID {task_id}")
        return (task, tasks)
