from .contracts.source import Source
from .contracts.task import Task
from .sources.file_source import FileSource
from .sources.generator_source import GeneratorSource
from .sources.json_source import JsonSource
from .sources.manual_input import ManualSource


def print_task(task: Task) -> None:
    print('\nTask added:')
    print(task)


def print_all_tasks(tasks: list) -> None:
    if not tasks:
        print('\nList of tasks is empty.')
        return

    print('\nAll tasks:')
    for task in tasks:
        print(task)


def create_source(choice: str) -> Source | None:
    if choice == '1':
        filename = input('Enter path to file: ')
        return FileSource(filename=filename)

    if choice == '2':
        return GeneratorSource()

    if choice == '3':
        json_name = input('Enter path to file: ')
        return JsonSource(json_name=json_name)

    if choice == '4':
        return ManualSource()
    return None


def print_menu() -> None:
    print('\nChoose action:')
    print('1 - Add task from file')
    print('2 - Generate random task')
    print('3 - Add task from json')
    print('4 - Add task manual')
    print('5 - Show all tasks')
    print('0 - Exit')
