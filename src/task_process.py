from typing import List

from src.task import TaskSource


def process_tasks(sources: List[TaskSource]) -> None:
    for source in sources:
        print("Source:", source.__class__)
        if not isinstance(source, TaskSource):
            print(source.__class__, "is wrong tasks source")
        tasks = source.get_tasks()
        print(f'Got {len(tasks)} tasks')
        [print(task) for task in tasks]
