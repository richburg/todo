import click

from todo.models import Task

from .database import Database
from .utilities import die, new_task_id_formula, warn

db = Database()


@click.group()
def cli():
    """Manage your tasks through the CLI"""
    pass


@cli.command()
@click.argument("description", type=str)
def add(description: str):
    """Add a new task"""
    with db as tasks:
        tasks.append(Task(new_task_id_formula(tasks), description))


@cli.command(name="ls")
def show():
    """List all your tasks"""
    with db as tasks:
        for task in tasks:
            info = f"\033[1m{task.id}\033[0m "
            if task.done:
                info += f"\033[9m{task.description}\033[0m"
            else:
                info += task.description
            click.echo(info)


@cli.command(name="rm")
@click.argument("ids", type=int, nargs=-1)
def remove(ids: list[int]):
    """Remove one or more task(s)"""
    with db as tasks:
        for id in ids:
            task = db.get(id)
            if task is None:
                warn(f"No task with ID {id}")
                continue
            tasks.remove(task)


@cli.command(name="ed")
@click.argument("id", type=int)
def edit(id: int):
    """Edit a task's description"""
    with db as _:
        task = db.get(id)
        if task is None:
            die(f"No task with ID {id}")
            return
        new_description = click.edit(task.description, "nano")
        if new_description is None:
            die("No changes made")
            return
        task.description = new_description.strip()


@cli.command(name="tg")
@click.argument("ids", type=int, nargs=-1)
def toggle(ids: list[int]):
    """Toggle done-status for one or more task(s)"""
    with db as _:
        for id in ids:
            task = db.get(id)
            if task is None:
                warn(f"No task with ID {id}")
                continue
            task.done = not task.done


@cli.command(name="st")
def sort():
    "Sort task IDs"
    with db as tasks:
        tasks.sort(key=lambda task: task.id and task.done)
        for index, task in enumerate(tasks, start=1):
            task.id = index
