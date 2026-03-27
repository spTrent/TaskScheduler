from typing import Any

from src.contracts.exceptions.exceptions import TaskInvalidSetValue


class StrDescriptor:
    def __set_name__(self, instance: Any, name: str) -> None:
        self.name = '_' + name

    def __get__(self, instance: Any, owner: Any) -> str:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise TaskInvalidSetValue(
                f'Attribute {self.name.strip("_")} must be a string'
            )
        setattr(instance, self.name, value)
