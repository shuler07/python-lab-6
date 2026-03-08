from os import PathLike
from typing import List, Any
import json
from random import randint, choice, choices, seed

from src.logger import logger
from src.task import Task
from src.constants import SEED


seed(SEED)

class TaskFileSource:
    def __init__(self, path: PathLike) -> None:
        tasks: List[dict[str, Any]] = []
        try:
            with open(file=path, mode='r') as f:
                tasks = json.load(f)
        except FileNotFoundError:
            print(f'File {path} not found')
            logger.warning('File %s not found', path)
            tasks = []
        self.tasks_iter = iter(tasks)
        self.path = path

    def get_tasks(self) -> List[Task]:
        tasks: List[Task] = []
        while (task := self.get_task()):
            tasks.append(task)
        logger.info('Got %d tasks from file source: %s', len(tasks), self.path)
        return tasks

    def get_task(self) -> Task | None:
        try:
            task_json = self.tasks_iter.__next__()
            task = Task(id=task_json['id'], payload=task_json['payload'])
            logger.info('Got task from file source: %s', self.path)
            return task
        except StopIteration:
            logger.info('No more tasks from file source: %s', self.path)
            return None


class TaskGeneratorSource:
    _words = ['some', 'random', 'words', 'home', 'task', \
              'action', 'give', 'length', 'music', 'work', \
                'free', 'stop', 'rating', 'bus', 'money',]
    def __init__(self) -> None:
        pass

    def get_tasks(self, amount: int = 10) -> List[Task]:
        tasks: List[Task] = []
        for _ in range(amount):
            tasks.append(self.get_task())
        logger.info('Got %d tasks from generator source', len(tasks))
        return tasks

    def get_task(self) -> Task:
        task = Task(id=randint(1, 99_999), payload=self._get_payload())
        logger.info('Got task from generator source')
        return task

    def _get_payload(self) -> Any:
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

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        tasks: List[Task] = []
        tasks_count = randint(1, 10)
        for _ in range(tasks_count):
            task = self.get_task()
            if task is not None:
                tasks.append(task)
        logger.info('Got %d tasks from API source', len(tasks))
        return tasks

    def get_task(self) -> Task | None:
        if randint(1, 5) != 1:
            task = Task(id=randint(1, 99_999), payload={'hardcoded': 'payload', 'useless': 'text', 'don\'t': 'read'})
            logger.info('Got task from API source')
        else:
            task = None
            logger.info('No task from API source')
        return task
