from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Task:
    id: int
    payload: Any
    deadline: datetime

    def __str__(self) -> str:
        return f"""Задача #{self.id}: {self.payload}
Deadline: {datetime.strftime(self.deadline, '%d.%m.%Y')}"""
