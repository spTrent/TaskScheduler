from .contracts.source import Source
from .interactive_funcs import (
    create_source,
    print_all_tasks,
    print_menu,
    print_task,
)
from .sources.file_source import FileSource
from .sources.generator_source import GeneratorSource
from .sources.json_source import JsonSource
from .sources.manual_input import ManualSource

sources: list = [
    ManualSource(),
    FileSource('test.txt'),
    GeneratorSource(),
    JsonSource('test.json'),
]
for source in sources:
    print(f'isinstance({source}, Source): {isinstance(source, Source)}')


def main() -> None:
    tasks: list = []
    print_menu()
    while (choice := input('Input operation: ').strip()) != '0':
        if choice == '5':
            print_all_tasks(tasks)
            print_menu()
            continue
        source = create_source(choice)
        if source is None:
            print('\nIncorrect operation')
            print_menu()
            continue
        try:
            task = source.get_task()
            tasks.append(task)
            print_task(task)
            print(f'Source: {source}')
        except FileNotFoundError:
            print('\nFile is not found.')
        except ValueError as error:
            print(str(error))
        except Exception as error:
            print(str(error))
        finally:
            print_menu()


if __name__ == '__main__':
    main()
