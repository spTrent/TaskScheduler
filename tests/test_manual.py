from unittest.mock import patch

import pytest

from src.contracts.task import Task
from src.sources.manual_input import ManualSource


def test_str():
    source = ManualSource()
    assert str(source) == 'Manual source'


def test_get_task_returns_expected_task():
    inputs = [
        '1',
        'Сделать лабу',
        '3',
        '',
        'no',
        '',
        '',
        '',
    ]

    with patch('builtins.input', side_effect=inputs):
        task = ManualSource().get_task()

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.title == 'Сделать лабу'
    assert task.priority == 3
    assert task.description == ''
    assert task.done is False
    assert task.done_at is None


def test_get_task_raises_error_for_invalid_id():
    inputs = ['abc', 'Сделать лабу', '15.03.2026']

    with patch('builtins.input', side_effect=inputs):
        with pytest.raises(ValueError):
            ManualSource().get_task()


def test_get_task_raises_error_for_invalid_date():
    inputs = ['1', 'Сделать лабу', '2026-03-15']

    with patch('builtins.input', side_effect=inputs):
        with pytest.raises(ValueError):
            ManualSource().get_task()
