from typing import Any

from src.contracts.exceptions.exceptions import TaskInvalidSetValue


class IntDescriptor:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.name: str = '_' + name

    def __get__(self, instance: Any, owner: Any) -> int | None:
        return getattr(instance, self.name, None)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TaskInvalidSetValue(
                f'Attribute {self.name.strip("_")} must be a integer'
            )
        setattr(instance, self.name, value)

    def __delete__(self, instance: Any) -> None:
        delattr(instance, self.name)
