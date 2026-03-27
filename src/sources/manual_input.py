from dataclasses import dataclass
from datetime import datetime, timezone

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
        task_id = int(input('Enter id: '))
        title = input('Enter title: ').strip()
        priority = int(input('Enter priority: ') or 1)
        description = input('Enter description (can be empty): ').strip()
        done = self._parse_bool(input('Is task done? (yes/no): ').strip())

        created_at = self._parse_datetime(
            input(
                'Enter date of creation in ISO-format '
                '(2026-03-27T12:00:00+00:00) or empty: '
            ).strip()
        )

        deadline = self._parse_datetime(
            input(
                'Enter deadline in ISO-format '
                '(2026-03-28T18:00:00+00:00) or empty: '
            ).strip()
        )

        done_at = self._parse_datetime(
            input(
                'Enter date of completion in ISO-format (can be empty): '
            ).strip()
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

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        if not value:
            return None

        dt = datetime.fromisoformat(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt

    @staticmethod
    def _parse_bool(value: str) -> bool:
        normalized = value.lower()

        if normalized in ('yes', 'y', 'true', '1', 'да', 'д'):
            return True
        if normalized in ('no', 'n', 'false', '0', 'нет', 'н'):
            return False

        raise ValueError('Input yes/no')

    def __str__(self) -> str:
        return 'Manual source'
