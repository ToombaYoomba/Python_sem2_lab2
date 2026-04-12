class TaskError(Exception):
    pass


class InvalidTaskIdError(TaskError):
    pass


class InvalidPriorityError(TaskError):
    pass


class InvalidStatusError(TaskError):
    pass


class InvalidDescriptionError(TaskError):
    pass


class ImmutableAttributeError(TaskError):
    pass