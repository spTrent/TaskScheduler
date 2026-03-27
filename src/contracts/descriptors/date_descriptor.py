from datetime import datetime
from typing import Any, Optional

from src.contracts.exceptions.exceptions import TaskInvalidSetValue


class DateDescriptor:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = '_' + name

    def __get__(self, instance: Any, owner: Any) -> Optional[datetime]:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: Optional[datetime]) -> None:
        if not isinstance(value, datetime) and value is not None:
            raise TaskInvalidSetValue(
                f'Attribute {self.name.strip("_")} must'
                'be a datetime object or None'
            )
        setattr(instance, self.name, value)
