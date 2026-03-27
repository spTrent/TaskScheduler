class TaskException(Exception):
    pass


class TaskInvalidSetValue(TaskException):
    pass


class TaskInvalidDeadline(TaskException):
    pass


class TaskInvalidStatus(TaskException):
    pass
