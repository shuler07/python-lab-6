from src.task_sources import TaskJsonSource, TaskGeneratorSource, TaskApiSource
from src.task_process import TaskProcessor


def main():
    "Main program"
    sources = []
    sources.append(TaskJsonSource(path='./example.json'))
    sources.append(TaskGeneratorSource())
    sources.append(TaskApiSource())

    task_processor = TaskProcessor()

    for source in sources:
        task_processor.process_task(source=source)
        task_processor.process_task(source=source)
        task_processor.process_task(source=source)


if __name__ == '__main__':
    main()
