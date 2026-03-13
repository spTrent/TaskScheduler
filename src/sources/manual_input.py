from dataclasses import dataclass
from datetime import datetime

from ..contracts.task import Task


@dataclass
class ManualSource:
    """
    Источник задач с помощью ручного ввода
    """
    def get_task(self) -> Task:
        """
        Запрашивает информацию о задаче и конструирует ее
        """
        id = int(input('Введите id задачи: '))
        payload = input('Введите задачу: ')
        deadline = datetime.strptime(
            input('Введите дедлайн(Пример: 18.03.2007): '), '%d.%m.%Y'
        )
        return Task(id=id, payload=payload, deadline=deadline)

    def __str__(self) -> str:
        return 'Ручная запись'
