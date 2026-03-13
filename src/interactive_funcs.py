from .sources.file_source import FileSource
from .sources.generator_source import GeneratorSource
from .sources.json_source import JsonSource
from .sources.manual_input import ManualSource

def print_task(task) -> None:
    print('\nДобавлена задача:')
    print(task)


def print_all_tasks(tasks: list) -> None:
    if not tasks:
        print('\nСписок задач пуст.')
        return

    print('\nВсе задачи:')
    for task in tasks:
        print(task)


def create_source(choice: str):
    if choice == '1':
        filename = input('Введите путь к txt-файлу: ')
        return FileSource(filename=filename)

    if choice == '2':
        return GeneratorSource()

    if choice == '3':
        json_name = input('Введите путь к JSON-файлу: ')
        return JsonSource(json_name=json_name)

    if choice == '4':
        return ManualSource()
    return None


def print_menu() -> None:
    print('\nВыберите действие:')
    print('1 — Добавить задачу из txt-файла')
    print('2 — Сгенерировать случайную задачу')
    print('3 — Добавить задачу из JSON-файла')
    print('4 — Добавить задачу вручную')
    print('5 — Показать все задачи')
    print('0 — Выход')

