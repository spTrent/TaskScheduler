from dataclasses import dataclass
from datetime import datetime

from ..contracts.task import Task


@dataclass
class FileSource:
    """
    Файловый источник задач
    """
    filename: str
    name: str | None = None

    def get_task(self) -> Task:
        """
        Открывает файл и возвращает сконструированную задачу из него
        """
        with open(self.filename) as file:
            text = file.read()
            id, payload, deadline = self.validate_text(text.split(':'))
            return Task(id=id, payload=payload, deadline=deadline)

    @staticmethod
    def validate_text(args: list) -> tuple:
        """
        Проверяет содержимое файла
        """
        if len(args) != 3:
            raise ValueError(
                'Неверный формат в файле (id:payload:day.month.year)'
            )
        id, payload, deadline = args
        return int(id), payload, datetime.strptime(deadline, '%d.%m.%Y')

    def __str__(self) -> str:
        return 'Файловый источник'
