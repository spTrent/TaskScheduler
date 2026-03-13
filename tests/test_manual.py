from datetime import datetime
from unittest.mock import patch

import pytest

from src.contracts.task import Task
from src.sources.manual_input import ManualSource


def test_str():
    source = ManualSource()
    assert str(source) == 'Ручная запись'


def test_get_task_returns_expected_task():
    inputs = ['1', 'Сделать лабу', '15.03.2026']

    with patch('builtins.input', side_effect=inputs):
        task = ManualSource().get_task()

    expected = Task(
        id=1,
        payload='Сделать лабу',
        deadline=datetime(2026, 3, 15),
    )
    assert task == expected


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
