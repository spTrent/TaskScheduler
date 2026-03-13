import json

import pytest

from src.contracts.task import Task
from src.sources.json_source import JsonSource


def test_str():
    source = JsonSource(json_name='task.json')

    assert str(source) == 'JSON-источник'


def test_get_task_returns_task_from_valid_json(tmp_path):
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'payload': 'Сделать лабу',
        'deadline': '15.03.2026',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))
    task = source.get_task()

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.payload == 'Сделать лабу'
    assert task.deadline == '15.03.2026'


def test_get_task_raises_error_if_id_is_missing(tmp_path):
    file_path = tmp_path / 'task.json'
    data = {
        'payload': 'Сделать лабу',
        'deadline': '15.03.2026',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(
        ValueError,
        match='Неверный формат JSON файла. Должны быть ключи id, payload, deadline',
    ):
        source.get_task()


def test_get_task_raises_error_if_payload_is_missing(tmp_path):
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'deadline': '15.03.2026',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(
        ValueError,
        match='Неверный формат JSON файла. Должны быть ключи id, payload, deadline',
    ):
        source.get_task()


def test_get_task_raises_error_if_deadline_is_missing(tmp_path):
    file_path = tmp_path / 'task.json'
    data = {
        'id': 1,
        'payload': 'Сделать лабу',
    }
    file_path.write_text(json.dumps(data), encoding='utf-8')

    source = JsonSource(json_name=str(file_path))

    with pytest.raises(
        ValueError,
        match='Неверный формат JSON файла. Должны быть ключи id, payload, deadline',
    ):
        source.get_task()
