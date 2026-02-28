from typing import List, Any
import json
from random import randint, choice, choices

from src.task import Task


class TaskFileSource:
    def __init__(self, path: str) -> None:
        if not isinstance(path, str):
            raise RuntimeError(f"Given wrong path - {path}")
        self.path = path

    def get_tasks(self) -> List[Task]:
        try:
            with open(self.path, mode='r') as f:
                tasks: List[Task] = json.load(f)
            return tasks
        except FileNotFoundError:
            print(f'File {self.path} not found')
            return []


class TaskGeneratorSource:
    _words = ['some', 'random', 'words', 'home', 'task', \
              'action', 'give', 'length', 'music', 'work', \
                'free', 'stop', 'rating', 'bus', 'money',]
    def __init__(self) -> None:
        pass

    def get_tasks(self, amount: int = 10) -> List[Task]:
        tasks: List[Task] = []
        for _ in range(amount):
            tasks.append(Task(id=randint(1, 99_999), payload=self._get_payload()))
        return tasks

    def _get_payload(self) -> Any:
        payload: Any
        match randint(1, 5):
            case 1:
                payload = randint(1, 100)
            case 2:
                payload = choice(self._words)
            case 3:
                payload = choices(self._words, k=randint(1, 5))
            case 4:
                payload = {choice(self._words): randint(1, 100), choice(self._words): choices(self._words, k=randint(1, 3))}
            case 5:
                payload = None
        return payload


class TaskApiSource:

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        tasks = [
            Task(id=randint(1, 99_999), payload={'hardcoded': 'payload', 'useless': 'text', 'don\'t': 'read'}),
            Task(id=randint(1, 99_999), payload='nothing useful'),
            Task(id=randint(1, 99_999), payload=[1, 2, 3, 4, 5, 6, 7])
        ]
        return tasks
