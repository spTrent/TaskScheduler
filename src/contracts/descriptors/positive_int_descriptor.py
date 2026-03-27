from typing import Any

from src.contracts.descriptors.int_descriptor import IntDescriptor
from src.contracts.exceptions.exceptions import TaskInvalidSetValue


class PositiveIntDescriptor(IntDescriptor):
    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise TaskInvalidSetValue(
                f'Attribute {self.name.strip("_")} must be a positive integer'
            )
        setattr(instance, self.name, value)
