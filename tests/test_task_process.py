import pytest
from pytest_mock import MockerFixture
import json
from pathlib import Path
from typing import List
from dataclasses import asdict

from src.task_sources import TaskApiSource, TaskFileSource, TaskGeneratorSource
from src.task_process import TaskProcessor
from src.task import Task


def get_random_tasks(n: int) -> List[Task]:
    return [Task(id=i, payload={"data": f"value{i}"}) for i in range(1, n + 1)]

@pytest.fixture
def test_json_file(tmp_path):
    file_path = tmp_path / "file.json"
    tasks = get_random_tasks(5)
    tasks_asdict = [asdict(task) for task in tasks]
    
    with open(file_path, "w") as f:
        json.dump(tasks_asdict, f)
    
    yield file_path


@pytest.fixture
def task_processor():
    return TaskProcessor()


def test_api_source(task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskApiSource()
    assert isinstance(source, TaskApiSource)
    
    tasks = source.get_tasks()
    assert isinstance(tasks, list)
    for task in tasks:
        assert isinstance(task, Task)
    
    task = source.get_task()
    assert isinstance(task, (Task, type(None)))

    mocked_print = mocker.patch("builtins.print")
    mocked_tasks = mocker.patch.object(source, "get_tasks", return_value=get_random_tasks(4))
    task_processor.process_tasks(source)
    mocked_tasks.assert_called_once()
    assert mocked_print.call_count == 5


def test_file_source(test_json_file: Path, task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskFileSource(test_json_file)
    assert isinstance(source, TaskFileSource)

    tasks = source.get_tasks()
    assert isinstance(tasks, list)
    for task in tasks:
        assert isinstance(task, Task)

    task = source.get_task()
    assert isinstance(task, (Task, type(None)))

    mocked_print = mocker.patch("builtins.print")
    task_processor.process_task(source)
    assert mocked_print.call_count == 2


def test_file_source_error():
    invalid_file = Path("non_existent_file.fake")
    assert not invalid_file.exists()

    source = TaskFileSource(invalid_file)
    assert isinstance(source, TaskFileSource)
    assert next(source.tasks_iter, None) is None


def test_generator_source(task_processor: TaskProcessor, mocker: MockerFixture):
    source = TaskGeneratorSource()
    assert isinstance(source, TaskGeneratorSource)

    tasks = source.get_tasks()
    assert isinstance(tasks, list)
    for task in tasks:
        assert isinstance(task, Task)
    
    task = source.get_task()
    assert isinstance(task, Task)

    mocked_print = mocker.patch("builtins.print")
    mocked_tasks = mocker.patch.object(source, "get_tasks", return_value=get_random_tasks(3))
    task_processor.process_tasks(source)
    mocked_tasks.assert_called_once()
    assert mocked_print.call_count == 4
    