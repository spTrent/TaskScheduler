from dataclasses import dataclass
from ..contracts.task import Task
from datetime import datetime

@dataclass
class ApiMock:
    def get_task(self) -> Task:
        id = int(input('Введите id задачи: '))
        payload = input('Введите задачу: ')
        deadline = datetime.strptime(input('Введите дедлайн(Пример: 18.03.2007): '), "%d.%m.%Y")
        return Task(id=id, payload=payload, deadline=deadline)
    
    def __str__(self):
        return 'API-заглушка'