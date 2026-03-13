import json
from ..contracts.task import Task
from dataclasses import dataclass

@dataclass
class JsonSource:
    json_name: str

    def get_task(self) -> Task:
        with open(self.json_name) as file:
            task_dict = json.load(file)
            if 'id' not in task_dict or 'payload' not in task_dict or 'deadline' not in task_dict:
                raise ValueError('Неверный формат JSON файла. Должны быть ключи id, payload, deadline')
            return Task(task_dict['id'], task_dict['payload'], task_dict['deadline'])
        
