from typing import Any, Protocol, runtime_checkable, Iterator, Literal
from datetime import datetime, timezone

from src.descriptors import ValidatedLiteral


TaskStatus = Literal['idle', 'active', 'done']
TaskPriority = Literal['low', 'medium', 'high', 'critical']


class Task:
    status = ValidatedLiteral(TaskStatus, "idle")
    priority = ValidatedLiteral(TaskPriority, "low")

    def __init__(self, id: int, payload: dict[str, Any]) -> None:
        self.id = id
        self.payload = payload

        self.description = payload.get("description", "Not provided")
        self.status = payload.get("status", "idle")
        self.priority = payload.get("priority", "low")

        self.created_at = datetime.now(timezone.utc)

    def __str__(self) -> str:
        return f"Task(id={self.id}, payload={self.payload}, description={self.description}, \
status={self.status}, priority={self.priority}, created_at={self.created_at})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise TypeError("Task description must be str")
        self._description = description


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterator[Task]: ...
    def get_task(self) -> Task | None: ...
