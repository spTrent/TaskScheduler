import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from ..contracts.task import Task


@dataclass
class GeneratorSource:
    """
    Генератор случайных задач
    """

    title_variants: list[str] = field(
        default_factory=lambda: [
            'Сделать лабу',
            'Сходить в зал',
            'Пройти урок по английскому',
            'Приготовить ужин',
            'Закончить pet-project',
            'Разобрать почту',
            'Подготовиться к собесу',
            'Прочитать главу книги',
        ]
    )

    description_variants: list[str] = field(
        default_factory=lambda: [
            '',
            'Сделать как можно раньше',
            'Не забыть проверить детали',
            'Разбить на маленькие шаги',
            'Сделать вечером',
        ]
    )

    def get_task(self) -> Task:
        """
        Генерирует и возвращает случайную задачу
        """

        now = datetime.now(timezone.utc)

        task_id = random.randint(1, 1_000_000)
        title = random.choice(self.title_variants)
        description = random.choice(self.description_variants)
        priority = random.randint(1, 5)

        created_at = now - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        done = random.choice([True, False])

        if done:
            done_at = created_at + timedelta(
                days=random.randint(0, 5),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            deadline = created_at + timedelta(
                days=random.randint(1, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
        else:
            done_at = None
            deadline = now + timedelta(
                days=random.randint(0, 7),
                hours=random.randint(1, 23),
                minutes=random.randint(0, 59),
            )

        return Task.create(
            id=task_id,
            title=title,
            priority=priority,
            description=description,
            done=done,
            created_at=created_at,
            deadline=deadline,
            done_at=done_at,
        )

    def __str__(self) -> str:
        return 'Random-Generator'
