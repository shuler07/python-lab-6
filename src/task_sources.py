from pathlib import Path
from typing import Any, Optional, Iterator
import json
from random import randint, choice, choices

from src.logger import logger
from src.task import Task


class TaskJsonSource:
    """
    Object for loading tasks by iterating over loaded list from json
    If file not found - warning message will be printed
    Args:
        path (PathLike): file path
    """
    def __init__(self, path: Optional[Path] = None) -> None:
        self.tasks_iter: Iterator[dict[str, Any]] = iter([])
        self.path = path
        if path is not None:
            self.open(path)

    def open(self, path: Path) -> None:
        self.path = path
        try:
            with open(file=path, mode='r') as f:
                loaded = json.load(f)
                if not isinstance(loaded, list):
                    raise TypeError
                self.tasks_iter = iter(loaded)
        except FileNotFoundError:
            print(f'File {path} not found')
            logger.warning('File %s not found', path)
        except TypeError:
            print(f'Json must contain list, but it contains {loaded.__class__.__name__}')
            logger.error('Json must contain list, but it contains %s', loaded.__class__.__name__)
        except json.JSONDecodeError:
            print(f'Json decode error. Check is file {path} correct')
            logger.error('Json decode error. Check is file %s correct', path)

    def get_tasks(self) -> Iterator[Task]:
        """
        Load tasks left in the file
        Returns:
            Iterator[Task]: tasks iterator
        """
        while (task := self.get_task()):
            yield task

    def get_task(self) -> Task | None:
        """
        Load next task from the file
        Returns:
            Task|None: Task object or None, if no task left in the file
        """
        try:
            task_json = self.tasks_iter.__next__()
            task = Task(id=task_json['id'], payload=task_json['payload'])
            logger.info('Got task from file source: %s', self.path)
            return task
        except StopIteration:
            logger.info('No more tasks from file source: %s', self.path)
            return None


class TaskGeneratorSource:
    """
    Object for generating random tasks
    """
    _words = ['some', 'random', 'words', 'home', 'task', \
              'action', 'give', 'length', 'music', 'work', \
                'free', 'stop', 'rating', 'bus', 'money',]
    def __init__(self) -> None:
        pass

    def get_tasks(self) -> Iterator[Task]:
        """
        Generate certain count of tasks
        Args:
            count (int): tasks count
        Returns:
            Iterator[Task]: tasks iterator
        """
        tasks_count = randint(1, 10)
        for _ in range(tasks_count):
            if (task := self.get_task()) is not None:
                yield task
        logger.info('Got %d tasks from generator source', tasks_count)

    def get_task(self) -> Task | None:
        """
        Generate task
        Returns:
            Task: generated task
        """
        if randint(1, 10) != 1:
            task = Task(id=randint(1, 99_999), payload=self._get_payload())
            logger.info('Got task from generator source')
            return task
        return None

    def _get_payload(self) -> dict[str, Any]:
        """
        Generate random payload for task
        Returns:
            dict[str,Any]: generated payload
        """
        payload: dict[str, Any] = {}
        payload_items_count = randint(1, 10)
        while len(payload) < payload_items_count:
            key = choice(self._words)
            if key in payload:
                continue
            match randint(1, 3):
                case 1:
                    payload[key] = randint(1, 100)
                case 2:
                    payload[key] = choice(self._words)
                case 3:
                    payload[key] = choices(self._words, k=randint(1, 5))
        return payload


class TaskApiSource:
    """
    Object for getting tasks from API
    """
    def __init__(self) -> None:
        pass

    def get_tasks(self) -> Iterator[Task]:
        """
        Get tasks from API
        Returns:
            Iterator[Task]: tasks
        """
        tasks_count = randint(1, 10)
        for _ in range(tasks_count):
            if (task := self.get_task()) is not None:
                yield task
        logger.info('Got %d tasks from API source', tasks_count)

    def get_task(self) -> Task | None:
        """
        Get task from API
        Returns:
            Task: task
        """
        if randint(1, 5) != 1:
            task = Task(id=randint(1, 99_999), payload={'hardcoded': 'payload', 'useless': 'text', 'don\'t': 'read'})
            logger.info('Got task from API source')
        else:
            task = None
            logger.info('No task from API source')
        return task
