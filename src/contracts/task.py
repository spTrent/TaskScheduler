from datetime import datetime, timedelta, timezone
from typing import Optional, Self

from src.contracts.descriptors.date_descriptor import DateDescriptor
from src.contracts.descriptors.int_descriptor import IntDescriptor
from src.contracts.descriptors.positive_int_descriptor import (
    PositiveIntDescriptor,
)
from src.contracts.descriptors.str_descriptor import StrDescriptor
from src.contracts.exceptions.exceptions import (
    TaskInvalidDeadline,
    TaskInvalidSetValue,
    TaskInvalidStatus,
)


class Task:
    id: IntDescriptor = IntDescriptor()
    title: StrDescriptor = StrDescriptor()
    priority: PositiveIntDescriptor = PositiveIntDescriptor()
    description: StrDescriptor = StrDescriptor()
    created_at: DateDescriptor = DateDescriptor()
    deadline: DateDescriptor = DateDescriptor()
    done_at: Optional[DateDescriptor] = DateDescriptor()

    def __init__(
        self,
        *,
        id: int,
        title: str,
        created_at: datetime,
        deadline: datetime,
        priority: int = 1,
        description: str = '',
        done: bool = False,
        done_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.title = title
        self.priority = priority
        self.description = description
        self.created_at = created_at
        self.deadline = deadline
        self.done = done
        self.done_at = done_at

    @property
    def is_ready_to_do(self) -> bool:
        if self.deadline is None:
            return not self.done
        return (not self.done) and datetime.now(timezone.utc) < self.deadline

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TaskInvalidSetValue('Attribute done must be a True/False')
        self._done = value

    @classmethod
    def create(
        cls,
        *,
        id: int,
        title: str,
        priority: int = 1,
        description: str = '',
        done: bool = False,
        created_at: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        done_at: Optional[datetime] = None,
    ) -> Self:
        if not done and done_at:
            raise TaskInvalidStatus('Task isnt done, but done_at exists')

        created_at = created_at or datetime.now(timezone.utc)
        deadline = deadline or created_at + timedelta(days=1)
        if done:
            done_at = done_at or datetime.now(timezone.utc)
        else:
            done_at = None

        if deadline < created_at:
            raise TaskInvalidDeadline('Deadline earlier than created_at')

        return cls(
            id=id,
            title=title,
            priority=priority,
            description=description,
            done=done,
            created_at=created_at,
            deadline=deadline,
            done_at=done_at,
        )

    def mark_done(self, done_at: Optional[datetime] = None) -> None:
        if self.created_at and done_at and done_at < self.created_at:
            raise TaskInvalidStatus('done_at earlier than created_at')
        self.done = True
        self.done_at = done_at or datetime.now(timezone.utc)

    def reopen(self, deadline: Optional[datetime] = None) -> None:
        now = datetime.now(timezone.utc)
        if deadline and deadline < now:
            raise TaskInvalidDeadline('Deadline earlier than now')

        if self.created_at and deadline and deadline < self.created_at:
            raise TaskInvalidDeadline('Deadline earlier than created_at')
        self.done = False
        self.done_at = None
        self.deadline = deadline or now + timedelta(days=1)

    def __str__(self) -> str:
        return f'Title: {self.title}\nDescription: {self.description}'
