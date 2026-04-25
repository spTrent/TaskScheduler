import pytest
from dataclasses import dataclass
from src.task_queue.task_queue import TaskQueue

@dataclass
class TaskMock:
    id: int
    done: bool
    priority: int


def test_task_queue_iteration():
    tasks = [TaskMock(1, False, 1), TaskMock(2, True, 2)]
    queue = TaskQueue(tasks)

    assert list(queue) == tasks


def test_task_queue_add_task():
    tasks = [TaskMock(1, False, 1)]
    queue = TaskQueue(tasks)
    new_task = TaskMock(2, True, 2)

    queue.add_task(new_task)

    assert list(queue) == [tasks[0], new_task]


def test_task_queue_filter_by_status():
    tasks = [TaskMock(1, False, 1), TaskMock(2, True, 2), TaskMock(3, True, 1)]
    queue = TaskQueue(tasks)

    filtered_queue = queue.filter_by_status(True)

    assert list(filtered_queue) == [tasks[1], tasks[2]]


def test_task_queue_filter_by_priority():
    tasks = [TaskMock(1, False, 1), TaskMock(2, True, 2), TaskMock(3, True, 1)]
    queue = TaskQueue(tasks)

    filtered_queue = queue.filter_by_priority(1)

    assert list(filtered_queue) == [tasks[0], tasks[2]]


def test_task_queue_chained_filters():
    tasks = [
        TaskMock(1, False, 1),
        TaskMock(2, True, 2),
        TaskMock(3, True, 1),
        TaskMock(4, False, 2)
    ]
    queue = TaskQueue(tasks)

    filtered_queue = queue.filter_by_status(True).filter_by_priority(1)

    assert list(filtered_queue) == [tasks[2]]


def test_task_queue_multiple_iterations():
    tasks = [TaskMock(1, False, 1), TaskMock(2, True, 2)]
    queue = TaskQueue(tasks)

    iteration_1 = list(queue)
    iteration_2 = list(queue)

    assert iteration_1 == iteration_2 == tasks


def test_filtered_queue_multiple_iterations():
    tasks = [TaskMock(1, False, 1), TaskMock(2, True, 2), TaskMock(3, True, 1)]
    queue = TaskQueue(tasks)

    filtered_queue = queue.filter_by_status(True)
    iteration_1 = list(filtered_queue)
    iteration_2 = list(filtered_queue)

    assert iteration_1 == iteration_2 == [tasks[1], tasks[2]]


def test_add_task_after_filter_creation():
    tasks = [TaskMock(1, False, 1)]
    queue = TaskQueue(tasks)

    filtered_queue = queue.filter_by_status(True)

    new_task = TaskMock(2, True, 2)
    queue.add_task(new_task)

    assert list(filtered_queue) == [new_task]