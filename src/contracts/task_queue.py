from typing import Generator, Protocol
from .task import Task

class TaskQueue(Protocol):
    def add_task(self, task: Task) -> None:
        ...

    def __getitem__(self, index: int) -> Task:
        ...

    def __iter__(self) -> 'TaskQueue':
        ...

    def __next__(self) -> Task:
        ...

    def filter_by_status(self, done: bool) -> Generator:
        ...

    def filter_by_priority(self, priority: int) -> Generator:
        ...

