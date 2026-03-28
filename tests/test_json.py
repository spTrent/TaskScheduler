import json
from datetime import datetime, timezone

import pytest

from src.contracts.task import Task
from src.sources.json_source import JsonSource


def test_str() -> None:
    source = JsonSource(json_name='task.json')
    assert str(source) == 'JSON-source from task.json'


def test_get_task_returns_task_from_valid_json(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'title': 'Do the lab assignment',
        'priority': 2,
        'description': 'Finish it today',
        'done': False,
        'created_at': '2026-03-14T10:00:00+00:00',
        'deadline': '2026-03-15T12:00:00+00:00',
        'done_at': None,
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))
    task = source.get_task()

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.title == 'Do the lab assignment'
    assert task.priority == 2
    assert task.description == 'Finish it today'
    assert task.done is False
    assert task.created_at == datetime(2026, 3, 14, 10, 0, 0, tzinfo=timezone.utc)
    assert task.deadline == datetime(2026, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
    assert task.done_at is None


def test_get_task_returns_task_from_minimal_valid_json(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'id': 2,
        'title': 'Go to the gym',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))
    task = source.get_task()

    assert isinstance(task, Task)
    assert task.id == 2
    assert task.title == 'Go to the gym'
    assert task.priority == 1
    assert task.description == ''
    assert task.done is False
    assert task.done_at is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.deadline, datetime)


def test_get_task_raises_error_if_id_is_missing(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'title': 'Do the lab assignment',
        'deadline': '2026-03-15T12:00:00+00:00',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(ValueError):
        source.get_task()


def test_get_task_raises_error_if_title_is_missing(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'deadline': '2026-03-15T12:00:00+00:00',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(ValueError):
        source.get_task()


def test_get_task_raises_error_if_datetime_has_invalid_format(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'title': 'Do the lab assignment',
        'deadline': '15.03.2026',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(ValueError):
        source.get_task()


def test_get_task_raises_error_if_deadline_is_not_string(tmp_path) -> None:
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'title': 'Do the lab assignment',
        'deadline': 12345,
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(
        ValueError,
        ):
        source.get_task()