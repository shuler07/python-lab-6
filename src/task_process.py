from src.logger import logger
from src.task import TaskSource


class TaskProcessor:
    """
    Object for processing tasks from different sources
    """
    def __init__(self):
        pass

    def _is_task_source_valid(self, source: TaskSource) -> bool:
        """
        Validate task source
        Returns:
            bool: is source valid
        """
        return isinstance(source, TaskSource)

    def process_tasks(self, source: TaskSource) -> None:
        """
        Process all tasks from source
        Args:
            source (TaskSource): source
        """
        if not self._is_task_source_valid(source):
            print("Object", source.__class__.__name__, "is wrong task source")
            logger.error("Object %s is wrong task source", source.__class__.__name__)
            return
        print(f"Proccessing tasks from object {source.__class__.__name__}")
        logger.info("Processing tasks from object %s", source.__class__.__name__)

        tasks = source.get_tasks()
        if len(tasks) > 0:
            for task in tasks:
                print(f"Task #{task.id} processed, payload: {task.payload}")
                logger.info("Task #%s processed", task.id)
        else:
            print("Tasks not found")

    def process_task(self, source: TaskSource) -> None:
        """
        Process task from source
        Args:
            source (TaskSource): source
        """
        if not self._is_task_source_valid(source):
            print("Object", source.__class__.__name__, "is wrong task source")
            logger.error("Object %s is wrong task source", source.__class__.__name__)
            return
        print(f"Proccessing task from object {source.__class__.__name__}")
        logger.info("Processing task from object %s", source.__class__.__name__)

        task = source.get_task()
        if task is not None:
            print(f"Task #{task.id} processed, payload: {task.payload}")
            logger.info("Task #%s processed", task.id)
        else:
            print("Task not found")
