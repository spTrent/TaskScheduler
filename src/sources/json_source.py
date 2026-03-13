import json
from dataclasses import dataclass

from ..contracts.task import Task


@dataclass
class JsonSource:
    """
    JSON-источник задач
    """
    json_name: str

    def get_task(self) -> Task:
        """
        Открывает JSON файл и извлекает задачу из него
        """
        with open(self.json_name) as file:
            task_dict = json.load(file)
            if (
                'id' not in task_dict
                or 'payload' not in task_dict
                or 'deadline' not in task_dict
            ):
                raise ValueError(
                    'Неверный формат JSON файла. Должны быть ключи id, payload, deadline'
                )
            return Task(
                task_dict['id'], task_dict['payload'], task_dict['deadline']
            )

    def __str__(self) -> str:
        return 'JSON-источник'
