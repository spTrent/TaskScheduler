from datetime import datetime

import pytest

from src.contracts.task import Task
from src.sources.file_source import FileSource


def test_validate_text():
    args = ['1', 'сделать дз', '15.03.2026']

    task_id, payload, deadline = FileSource.validate_text(args)

    assert task_id == 1
    assert payload == 'сделать дз'
    assert deadline == datetime(2026, 3, 15)


def test_validate_text_raises():
    args = ['1', 'сделать дз']

    with pytest.raises(ValueError, match='Неверный формат в файле'):
        FileSource.validate_text(args)


def test_correct_task(tmp_path):
    file_path = tmp_path / 'task.txt'
    file_path.write_text('1:сделать дз:15.03.2026', encoding='utf-8')

    source = FileSource(filename=str(file_path))
    task = source.get_task()

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.payload == 'сделать дз'
    assert task.deadline == datetime(2026, 3, 15)


def test_get_task_raises_error_for_invalid_file_content(tmp_path):
    file_path = tmp_path / 'task.txt'
    file_path.write_text('1:сделать дз', encoding='utf-8')

    source = FileSource(filename=str(file_path))

    with pytest.raises(ValueError, match='Неверный формат в файле'):
        source.get_task()
