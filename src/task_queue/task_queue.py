from typing import Generator, Iterable, Callable
import itertools

from src.contracts.task import Task


class LazyFilter:
    def __init__(self, iterable: Iterable[Task] | None, predicate: Callable[[Task], bool]):
        self._iterable = iterable or []
        self._predicate = predicate

    def __iter__(self) -> Generator:
        for task in self._iterable:
            if self._predicate(task):
                yield task


class TaskQueue:
    def __init__(self, tasks: Iterable[Task] | None):
        self._base_tasks = tasks or []
        self._added_tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self._added_tasks.append(task)

    def __iter__(self) -> Generator:
        iterator = itertools.chain(self._base_tasks, self._added_tasks)
        yield from iterator

    def filter_by_status(self, done: bool) -> 'TaskQueue':
        lazy_iterable = LazyFilter(self, lambda t: t.done == done)
        return TaskQueue(lazy_iterable)

    def filter_by_priority(self, priority: int) -> 'TaskQueue':
        lazy_iterable = LazyFilter(self, lambda t: t.priority == priority)
        return TaskQueue(lazy_iterable)
