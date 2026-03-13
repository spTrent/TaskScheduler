from dataclasses import dataclasss
from ..contracts.task import Task
from datetime import datetime

def validate_text(args):
    if len(args) != 3:
        raise ValueError("Неверный формат в файле (id:payload:day.month.year)")
    id, payload, deadline = args
    return int(id), payload, datetime.strptime(deadline, '%d.%m.%Y')


@dataclasss
class FileSource:
    filename: str
    name: str | None = None

    def get_task(self) -> Task:
        with open(self.filename) as file:
            text = file.read()
            id, payload, deadline = validate_text(text.split(':'))
            return Task(id=id, payload=payload, deadline=deadline)
