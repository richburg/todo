import click

from todo.database import Database, Task
from todo.helpers import get_data_file

db = Database(get_data_file())


@click.group()
def cli() -> None:
    pass


@cli.command()
def show():
    tasks = db.load_tasks()
    for task in tasks:
        info = f"\033[1m{task.id}\033[0m "
        if task.done:
            info += f"\033[9m{task.description}\033[0m"
        else:
            info += task.description
        click.echo(info)


@cli.command()
@click.argument("description", type=str)
def add(description: str):
    tasks = db.load_tasks()
    if tasks:
        new_task_id: int = max(task.id for task in tasks) + 1
    else:
        new_task_id = 1
    new_task = Task(id=new_task_id, description=description)
    tasks.append(new_task)
    db.save_tasks(tasks)


@cli.command()
@click.argument("ids", type=int, nargs=-1)
def remove(ids: list[int]):
    for id in ids:
        task, tasks = db.find_task(id)
        if task:
            tasks.remove(task)
            db.save_tasks(tasks)


@cli.command()
@click.argument("ids", type=int, nargs=-1)
def toggle(ids: list[int]):
    for id in ids:
        task, tasks = db.find_task(id)
        if task:
            task.done = not task.done
        db.save_tasks(tasks)


@cli.command()
def sort():
    tasks = db.load_tasks()
    tasks.sort(key=lambda task: task.id and task.done)
    # Keep in mind that .sort() doesn't change any value except ordering them in the array.
    # In this code block, we are changing their IDs based on their array index.
    for index, task in enumerate(tasks, start=1):
        task.id = index
    db.save_tasks(tasks)


@cli.command()
@click.argument("id", type=int)
def edit(id: int):
    task, tasks = db.find_task(id)
    if task:
        new_content = click.edit(task.description, "nano")
        if not new_content:
            return
        task.description = new_content.strip()
        db.save_tasks(tasks)


if __name__ == "__main__":
    cli()
