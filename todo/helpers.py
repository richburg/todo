import os
import sys
from pathlib import Path
from typing import Optional

from click import echo


def warning(message: str) -> None:
    echo(f"\033[33mwarning\033[0m: {message}")


def die(message: str) -> None:
    echo(f"\033[31merror\033[0m: {message}")
    sys.exit(1)


def get_data_file() -> Path:
    provided_file_path: Optional[str] = os.getenv("TODO_DATA_FILE", "~/.tasks.json")
    file = Path(provided_file_path).expanduser()  # type: ignore

    if not file.exists():
        file.touch()
        file.write_text("[]")

    return file
