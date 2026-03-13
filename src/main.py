from .contracts.source import Source
from .sources.file_source import FileSource
from .sources.generator_source import GeneratorSource
from .sources.json_source import JsonSource
from .sources.manual_input import ManualSource
from .interactive_funcs import print_all_tasks, print_menu, print_task, create_source

sources: list = [
    ManualSource(),
    FileSource('test.txt'),
    GeneratorSource(),
    JsonSource('test.json'),
]
for source in sources:
    print(f'isinstance({source}, Source): {isinstance(source, Source)}')


def main() -> None:
    tasks = []
    print_menu()
    while ((choice := input('Введите операцию: ').strip()) != '0'):
        if choice == '5':
            print_all_tasks(tasks)
            print_menu()
            continue
        source = create_source(choice)
        if source is None:
            print('\nНеверный пункт меню. Попробуйте снова.')
            print_menu()
            continue
        try:
            task = source.get_task()
            tasks.append(task)
            print_task(task)
            print(f'Источник: {source}')
        except FileNotFoundError:
            print('\nФайл не найден.')
        except ValueError as error:
            print(f'\nОшибка данных: {error}')
        except Exception as error:
            print(f'\nНепредвиденная ошибка: {error}')
        finally:
            print_menu()
        


if __name__ == '__main__':
    main()