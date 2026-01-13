import click

from .models import Task


def die(message: str) -> None:
    """Log and exit the program"""
    click.echo(f"\033[31merror\033[0m: {message}")
    exit(1)


def warn(message: str) -> None:
    """Log a warning"""
    click.echo(f"\033[33mwarning\033[0m: {message}")


def new_task_id_formula(tasks: list[Task]) -> int:
    """Formula for new task ID"""
    if not tasks:
        return 1
    result: int = max(task.id for task in tasks) + 1
    return result
