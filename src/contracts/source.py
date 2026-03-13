from typing import Protocol, runtime_checkable
from .task import Task

@runtime_checkable
class Source(Protocol):
    def get_task(self) -> Task:
        pass