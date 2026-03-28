from src.contracts.task import Task
from src.sources.generator_source import GeneratorSource


def test_str():
    source = GeneratorSource()
    assert str(source) == 'Random-Generator'


def test_get_task_returns_task():
    source = GeneratorSource()
    task = source.get_task()
    assert isinstance(task, Task)
