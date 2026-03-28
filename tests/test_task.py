import pytest
from datetime import datetime, timedelta, timezone

from src.contracts.task import Task
from src.contracts.exceptions.exceptions import (
    TaskInvalidDeadline,
    TaskInvalidSetValue,
    TaskInvalidStatus,
)


def utc_dt(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
) -> datetime:
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


def test_create_task_with_required_fields() -> None:
    task = Task.create(
        id=1,
        title='Finish homework',
    )

    assert task.id == 1
    assert task.title == 'Finish homework'
    assert task.priority == 1
    assert task.description == ''
    assert task.done is False
    assert task.done_at is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.deadline, datetime)
    assert task.deadline > task.created_at


def test_create_task_with_all_fields() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    deadline = created_at + timedelta(days=2)
    done_at = created_at + timedelta(hours=5)

    task = Task.create(
        id=2,
        title='Go to the gym',
        priority=3,
        description='Leg day',
        done=True,
        created_at=created_at,
        deadline=deadline,
        done_at=done_at,
    )

    assert task.id == 2
    assert task.title == 'Go to the gym'
    assert task.priority == 3
    assert task.description == 'Leg day'
    assert task.done is True
    assert task.created_at == created_at
    assert task.deadline == deadline
    assert task.done_at == done_at


def test_create_task_sets_done_at_automatically_when_done() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    deadline = created_at + timedelta(days=1)

    task = Task.create(
        id=3,
        title='Cook dinner',
        done=True,
        created_at=created_at,
        deadline=deadline,
    )

    assert task.done is True
    assert task.done_at is not None
    assert task.done_at >= created_at


def test_create_raises_when_done_is_false_but_done_at_exists() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    done_at = created_at + timedelta(hours=1)

    with pytest.raises(TaskInvalidStatus):
        Task.create(
            id=4,
            title='Read a book',
            done=False,
            created_at=created_at,
            done_at=done_at,
        )


def test_create_raises_when_deadline_is_earlier_than_created_at() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    deadline = created_at - timedelta(hours=1)

    with pytest.raises(TaskInvalidDeadline):
        Task.create(
            id=5,
            title='Prepare for interview',
            created_at=created_at,
            deadline=deadline,
        )


def test_done_setter_accepts_bool() -> None:
    task = Task.create(id=6, title='Task')

    task.done = True
    assert task.done is True

    task.done = False
    assert task.done is False


def test_done_setter_raises_for_non_bool() -> None:
    task = Task.create(id=7, title='Task')

    with pytest.raises(TaskInvalidSetValue):
        task.done = 'yes'


def test_mark_done_sets_done_and_done_at() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    task = Task.create(
        id=8,
        title='Finish pet project',
        created_at=created_at,
    )

    done_at = created_at + timedelta(hours=2)
    task.mark_done(done_at)

    assert task.done is True
    assert task.done_at == done_at


def test_mark_done_without_argument_sets_current_done_at() -> None:
    task = Task.create(
        id=9,
        title='Check emails',
    )

    task.mark_done()

    assert task.done is True
    assert task.done_at is not None


def test_mark_done_raises_when_done_at_is_earlier_than_created_at() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    task = Task.create(
        id=10,
        title='Study English',
        created_at=created_at,
    )

    invalid_done_at = created_at - timedelta(minutes=1)

    with pytest.raises(TaskInvalidStatus):
        task.mark_done(invalid_done_at)


def test_reopen_resets_done_and_done_at_and_sets_new_deadline() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    deadline = created_at + timedelta(days=1)
    done_at = created_at + timedelta(hours=3)

    task = Task.create(
        id=11,
        title='Workout',
        done=True,
        created_at=created_at,
        deadline=deadline,
        done_at=done_at,
    )

    new_deadline = utc_dt(2026, 3, 30, 12, 0, 0)
    task.reopen(new_deadline)

    assert task.done is False
    assert task.done_at is None
    assert task.deadline == new_deadline


def test_reopen_without_deadline_sets_future_deadline() -> None:
    task = Task.create(
        id=12,
        title='Lab assignment',
        done=True,
    )

    old_deadline = task.deadline
    task.reopen()

    assert task.done is False
    assert task.done_at is None
    assert task.deadline > datetime.now(timezone.utc)
    assert task.deadline != old_deadline


def test_reopen_raises_when_deadline_is_in_past() -> None:
    task = Task.create(
        id=13,
        title='Task',
    )

    past_deadline = datetime.now(timezone.utc) - timedelta(hours=1)

    with pytest.raises(TaskInvalidDeadline):
        task.reopen(past_deadline)


def test_reopen_raises_when_deadline_is_earlier_than_created_at() -> None:
    created_at = utc_dt(2026, 3, 28, 10, 0, 0)
    task = Task.create(
        id=14,
        title='Task',
        created_at=created_at,
    )

    invalid_deadline = created_at - timedelta(minutes=1)

    with pytest.raises(TaskInvalidDeadline):
        task.reopen(invalid_deadline)


def test_is_ready_to_do_returns_true_for_not_done_task_before_deadline() -> None:
    task = Task.create(
        id=15,
        title='Active task',
        created_at=datetime.now(timezone.utc),
        deadline=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    assert task.is_ready_to_do is True


def test_is_ready_to_do_returns_false_for_done_task() -> None:
    task = Task.create(
        id=16,
        title='Completed task',
        done=True,
    )

    assert task.is_ready_to_do is False


def test_is_ready_to_do_returns_false_for_expired_task() -> None:
    now = datetime.now(timezone.utc)
    task = Task.create(
        id=17,
        title='Expired task',
        created_at=now - timedelta(days=2),
        deadline=now - timedelta(hours=1),
    )

    assert task.is_ready_to_do is False


def test_str_returns_title_and_description() -> None:
    task = Task.create(
        id=18,
        title='Read chapter',
        description='Chapter 5 of the book',
    )

    result = str(task)

    assert 'Title: Read chapter' in result
    assert 'Description: Chapter 5 of the book' in result