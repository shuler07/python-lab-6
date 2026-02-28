from typing import Any, Protocol, runtime_checkable, List
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    payload: Any


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> List[Task]: ...
