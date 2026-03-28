from datetime import datetime, timezone

import pytest

from src.contracts.task import Task
from src.sources.file_source import FileSource


def test_parse_returns_valid_data() -> None:
    text = '1:do homework:30.03.2026'

    task_id, title, deadline = FileSource._parse(text)

    assert task_id == 1
    assert title == 'do homework'
    assert deadline == datetime(2026, 3, 30, tzinfo=timezone.utc)


def test_parse_raises_for_invalid_format() -> None:
    text = '1:do homework'

    with pytest.raises(ValueError):
        FileSource._parse(text)


def test_parse_raises_for_invalid_id() -> None:
    text = 'abc:do homework:15.03.2026'

    with pytest.raises(ValueError):
        FileSource._parse(text)


def test_parse_raises_for_invalid_date() -> None:
    text = '1:do homework:2026-03-15'

    with pytest.raises(ValueError):
        FileSource._parse(text)


def test_get_task_returns_correct_task(tmp_path) -> None:
    file_path = tmp_path / 'task.txt'
    file_path.write_text('1:do homework:30.03.2026', encoding='utf-8')

    source = FileSource(filename=str(file_path))
    task = source.get_task()

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.title == 'do homework'
    assert task.deadline == datetime(2026, 3, 30, tzinfo=timezone.utc)
    assert task.done is False
    assert task.done_at is None


def test_get_task_raises_for_invalid_file_content(tmp_path) -> None:
    file_path = tmp_path / 'task.txt'
    file_path.write_text('1:do homework', encoding='utf-8')

    source = FileSource(filename=str(file_path))

    with pytest.raises(ValueError):
        source.get_task()