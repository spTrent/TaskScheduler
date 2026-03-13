from dataclasses import dataclass
from typing import Any
from datetime import datetime

@dataclass
class Task:
    id: int
    payload: Any
    deadline: datetime

    def __str__(self):
        return f'Задача #{self.id}: {self.payload}\nDeadline: {datetime.strftime(self.deadline, "%d.%m.%Y")}'
    