import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..contracts.task import Task


@dataclass
class JsonSource:
    """
    JSON-источник задач
    """

    json_name: str

    def get_task(self) -> Task:
        """
        Открывает JSON-файл и извлекает задачу из него
        """
        with open(self.json_name, encoding='utf-8') as file:
            task_dict = json.load(file)

        return self._build_task(task_dict)

    @staticmethod
    def _build_task(task_dict: dict[str, Any]) -> Task:
        """
        Проверяет JSON и создает Task
        """

        if 'id' not in task_dict:
            raise ValueError('In JSON miss "id"')
        if 'title' not in task_dict:
            raise ValueError('In JSON miss "title"')

        created_at = JsonSource._parse_datetime(task_dict.get('created_at'))
        deadline = JsonSource._parse_datetime(task_dict.get('deadline'))
        done_at = JsonSource._parse_datetime(task_dict.get('done_at'))

        return Task.create(
            id=task_dict['id'],
            title=task_dict['title'],
            priority=task_dict.get('priority', 1),
            description=task_dict.get('description', ''),
            done=task_dict.get('done', False),
            created_at=created_at,
            deadline=deadline,
            done_at=done_at,
        )

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        """
        Преобразует строку из JSON в datetime
        """
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError('Date must be in ISO-Format or None')

        try:
            return datetime.fromisoformat(value)
        except ValueError as err:
            raise ValueError(
                f'Invalid format of date: {value}. Expected ISO'
            ) from err

    def __str__(self) -> str:
        return f'JSON-source from {self.json_name}'
