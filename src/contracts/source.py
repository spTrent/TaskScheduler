from typing import Protocol
from .task import Task

class Source(Protocol):
    def get_task(self) -> Task:
        pass