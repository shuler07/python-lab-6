import typer
from typing import Annotated, Literal, Optional, List
from pathlib import Path

from src.task_sources import TaskJsonSource, TaskGeneratorSource, TaskApiSource
from src.task_process import TaskProcessor
from src.task import Task, TaskSource


app = typer.Typer(name='...', help='...')
task_app = typer.Typer(name='task', help='...')

task_processor = TaskProcessor()
task_generator_source = TaskGeneratorSource()
task_json_source = TaskJsonSource()
task_api_source = TaskApiSource()


def get_from_source(source: TaskSource, is_all_tasks: bool) -> Task | List[Task] | None:
    return source.get_tasks() if is_all_tasks else source.get_task()

def process_from_source(source: TaskSource, is_all_tasks: bool) -> None:
    return task_processor.process_tasks(source) if is_all_tasks else task_processor.process_task(source)


@task_app.command(name='get', help='...')
def task_get(
    source: Annotated[Literal['generator', 'api', 'json'], typer.Argument(help='...')] = 'generator',
    path: Annotated[Optional[Path], typer.Option('-p', '--path', help='...')] = None,
    is_all_tasks: Annotated[bool, typer.Option('-a', '--all', help='...')] = False,
):
    data: Task | List[Task] | None
    match source:
        case 'generator':
            data = get_from_source(task_generator_source, is_all_tasks)
        case 'api':
            data = get_from_source(task_api_source, is_all_tasks)
        case 'json':
            if path is None:
                raise typer.BadParameter('Json task source requires -p / --path parameter')
            if not str(path).endswith('.json'):
                raise typer.BadParameter('Expected .json file')
            task_json_source.open(path)
            data = get_from_source(task_json_source, is_all_tasks)

    if isinstance(data, Task):
        typer.echo(data)
    elif isinstance(data, list):
        for task in data:
            typer.echo(task)
    else:
        typer.echo("No task")


@task_app.command(name='process', help='...')
def task_process(
    source: Annotated[Literal['generator', 'api', 'json'], typer.Argument(help='...')] = 'generator',
    path: Annotated[Optional[Path], typer.Option('-p', '--path', help='...')] = None,
    is_all_tasks: Annotated[bool, typer.Option(..., '-a', '--all')] = False
):
    match source:
        case 'generator':
            process_from_source(task_generator_source, is_all_tasks)
        case 'api':
            process_from_source(task_api_source, is_all_tasks)
        case 'json':
            if path is None:
                raise typer.BadParameter('Json task source requires -p / --path parameter')
            if not str(path).endswith('.json'):
                raise typer.BadParameter('Expected .json file')
            task_json_source.open(path)
            process_from_source(task_json_source, is_all_tasks)


app.add_typer(task_app)
