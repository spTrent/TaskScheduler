from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from ..contracts.task import Task


@dataclass
class FileSource:
    """
    Файловый источник задач
    """

    filename: str
    name: Optional[str] = None

    def get_task(self) -> Task:
        """
        Открывает файл и возвращает задачу
        Формат файла: id:title:deadline (day.month.year)
        """
        with open(self.filename, encoding='utf-8') as file:
            text = file.read().strip()

        id, title, deadline = self._parse(text)

        return Task.create(
            id=id,
            title=title,
            deadline=deadline,
        )

    @staticmethod
    def _parse(text: str) -> tuple[int, str, datetime]:
        """
        Парсит и валидирует содержимое файла
        """
        parts = text.split(':')

        if len(parts) != 3:
            raise ValueError(
                'Invalid format in file (id:title:day.month.year)'
            )

        raw_id, title, raw_deadline = parts

        try:
            task_id = int(raw_id)
        except ValueError as err:
            raise ValueError('id must be a integer') from err

        try:
            deadline = datetime.strptime(raw_deadline, '%d.%m.%Y')
            deadline = deadline.replace(tzinfo=timezone.utc)
        except ValueError as err:
            raise ValueError(
                'Invalid format in date (expected dd.mm.yyyy)'
            ) from err

        return task_id, title, deadline

    def __str__(self) -> str:
        return f'File Source from {self.filename}'
