import pytest
from pytest_mock import MockerFixture
import json
from pathlib import Path
from typing import Iterator, cast, Iterable, List

from src.task_sources import TaskApiSource, TaskJsonSource, TaskGeneratorSource
from src.task_process import TaskProcessor
from src.task import Task, TaskSource


def get_random_tasks(n: int) -> Iterator[Task]:
    """
    Generator containing n tasks
    Args:
        n (int): count
    Returns:
        Iterator[Task]: tasks generator
    """
    return (Task(id=i, payload={"data": f"value{i}"}) for i in range(1, n + 1))

@pytest.fixture
def test_json_file(tmp_path):
    "Creates temporary json file"
    file_path = tmp_path / "file.json"
    tasks: List[Task] = []
    for task in get_random_tasks(5):
        tasks.append({
            'id': task.id,
            'payload': task.payload,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'ts_created_at': task.ts_created_at
        })

    with open(file_path, "w") as f:
        json.dump(tasks, f)

    yield file_path


@pytest.fixture
def task_processor():
    "Creates TaskProcessor object"
    return TaskProcessor()


def test_api_source(task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskApiSource()
    assert isinstance(source, TaskApiSource)

    tasks = source.get_tasks()
    assert isinstance(tasks, Iterable)
    for task in tasks:
        assert isinstance(task, Task)

    new_task = source.get_task()
    assert isinstance(new_task, (Task, type(None)))

    mocked_print = mocker.patch("builtins.print")
    mocked_tasks = mocker.patch.object(source, "get_tasks", return_value=get_random_tasks(4))
    task_processor.process_tasks(cast(TaskSource, source))
    mocked_tasks.assert_called_once()
    assert mocked_print.call_count == 5


def test_file_source(test_json_file: Path, task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskJsonSource(test_json_file)
    assert isinstance(source, TaskJsonSource)

    tasks = source.get_tasks()
    assert isinstance(tasks, Iterable)
    for task in tasks:
        assert isinstance(task, Task)

    new_task = source.get_task()
    assert isinstance(new_task, (Task, type(None)))

    mocked_print = mocker.patch("builtins.print")
    task_processor.process_task(cast(TaskSource, source))
    assert mocked_print.call_count == 2


def test_file_source_error():
    invalid_file = Path("non_existent_file.fake")
    assert not invalid_file.exists()

    source = TaskJsonSource(invalid_file)
    assert isinstance(source, TaskJsonSource)
    assert next(source.tasks_iter, None) is None


def test_generator_source(task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskGeneratorSource()
    assert isinstance(source, TaskGeneratorSource)

    tasks = source.get_tasks()
    assert isinstance(tasks, Iterable)
    for task in tasks:
        assert isinstance(task, Task)

    new_task = source.get_task()
    assert isinstance(new_task, Task)

    mocked_print = mocker.patch("builtins.print")
    mocked_tasks = mocker.patch.object(source, "get_tasks", return_value=get_random_tasks(3))
    task_processor.process_tasks(cast(TaskSource, source))
    mocked_tasks.assert_called_once()
    assert mocked_print.call_count == 4
