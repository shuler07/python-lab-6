from src.task_sources import TaskFileSource, TaskGeneratorSource, TaskApiSource
from src.task_process import process_tasks


def main():
    sources = []
    sources.append(TaskFileSource(path='./data.json'))
    sources.append(TaskGeneratorSource())
    sources.append(TaskApiSource())

    process_tasks(sources)


if __name__ == '__main__':
    main()
