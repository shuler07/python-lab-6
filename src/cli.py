import typer
from typing import Annotated, Literal, Optional, Iterator, Iterable
from pathlib import Path

from src.task_sources import TaskJsonSource, TaskGeneratorSource, TaskApiSource
from src.task_process import TaskProcessor
from src.task import Task


app = typer.Typer(name='Tasker', help='Platform to work with tasks')
task_app = typer.Typer(name='task', help='Task processing')

task_processor = TaskProcessor()
task_generator_source = TaskGeneratorSource()
task_json_source = TaskJsonSource()
task_api_source = TaskApiSource()


@task_app.command(name='get', help='Get tasks from source')
def task_get(
    source: Annotated[Literal['generator', 'api', 'json'], typer.Argument(help='Task source')] = 'generator',
    path: Annotated[Optional[Path], typer.Option('-p', '--path', help='Filepath (using only with json source)')] = None,
    is_all_tasks: Annotated[bool, typer.Option('-a', '--all', help='Get all possible tasks')] = False,
):
    data: Task | Iterator[Task] | None
    match source:
        case 'generator':
            if is_all_tasks:
                data = task_generator_source.get_tasks()
            else:
                data = task_generator_source.get_task()
        case 'api':
            if is_all_tasks:
                data = task_api_source.get_tasks()
            else:
                data = task_api_source.get_task()
        case 'json':
            if path is None:
                raise typer.BadParameter('Json task source requires -p / --path parameter')
            if not str(path).endswith('.json'):
                raise typer.BadParameter('Expected .json file')
            task_json_source.open(path)
            if is_all_tasks:
                data = task_json_source.get_tasks()
            else:
                data = task_json_source.get_task()

    if isinstance(data, Task):
        typer.echo(data)
    elif isinstance(data, Iterable):
        for task in data:
            typer.echo(task)
    else:
        typer.echo("No task")


@task_app.command(name='process', help='Process tasks from source')
def task_process(
    source: Annotated[Literal['generator', 'api', 'json'], typer.Argument(help='Tasks source')] = 'generator',
    path: Annotated[Optional[Path], typer.Option('-p', '--path', help='Filepath (using only with json source)')] = None,
    is_all_tasks: Annotated[bool, typer.Option(..., '-a', '--all', help='Process all possible tasks')] = False
):
    match source:
        case 'generator':
            if is_all_tasks:
                task_processor.process_tasks(task_generator_source)
            else:
                task_processor.process_task(task_generator_source)
        case 'api':
            if is_all_tasks:
                task_processor.process_tasks(task_api_source)
            else:
                task_processor.process_task(task_api_source)
        case 'json':
            if path is None:
                raise typer.BadParameter('Json task source requires -p / --path parameter')
            if not str(path).endswith('.json'):
                raise typer.BadParameter('Expected .json file')
            task_json_source.open(path)
            if is_all_tasks:
                task_processor.process_tasks(task_json_source)
            else:
                task_processor.process_task(task_json_source)


app.add_typer(task_app)
