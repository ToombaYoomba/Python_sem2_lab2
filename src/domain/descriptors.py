from datetime import datetime
from typing import Any, TypeVar, Generic

from src.domain.exceptions import (
    InvalidTaskIdError,
    InvalidPriorityError,
    InvalidStatusError,
    InvalidDescriptionError,
    ImmutableAttributeError,
)

T = TypeVar('T')


class ValidatedAttribute(Generic[T]):
    def __init__(self, name: str, validator: callable, immutable: bool = False):
        self.name = f"_{name}"
        self.validator = validator
        self.immutable = immutable

    def __get__(self, instance: Any, owner: Any) -> T:
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance: Any, value: T) -> None:
        if self.immutable and hasattr(instance, self.name):
            raise ImmutableAttributeError(
                f"Attribute '{self.name[1:]}' is immutable and cannot be modified"
            )
        validated_value = self.validator(value)
        setattr(instance, self.name, validated_value)

    def __delete__(self, instance: Any) -> None:
        raise ImmutableAttributeError(f"Cannot delete attribute '{self.name[1:]}'")


class CachedProperty(Generic[T]):
    def __init__(self, func):
        self.func = func
        self.name = f"_cached_{func.__name__}"

    def __get__(self, instance: Any, owner: Any) -> T:
        if instance is None:
            return self

        if not hasattr(instance, self.name):
            value = self.func(instance)
            setattr(instance, self.name, value)

        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError(
            f"Cached property '{self.func.__name__}' is read-only"
        )


def validate_task_id(value: Any) -> str:
    if not isinstance(value, str):
        raise InvalidTaskIdError(f"Task id must be str, got {type(value).__name__}")
    if not value.strip():
        raise InvalidTaskIdError("Task id cannot be empty or whitespace")
    if len(value) > 100:
        raise InvalidTaskIdError(f"Task id too long: {len(value)} > 100")
    return value.strip()


def validate_description(value: Any) -> str:
    if not isinstance(value, str):
        raise InvalidDescriptionError(f"Description must be str, got {type(value).__name__}")
    if len(value.strip()) < 3:
        raise InvalidDescriptionError("Description must be at least 3 characters")
    if len(value) > 1000:
        raise InvalidDescriptionError(f"Description too long: {len(value)} > 1000")
    return value.strip()


def validate_priority(value: Any) -> int:
    if not isinstance(value, int):
        raise InvalidPriorityError(f"Priority must be int, got {type(value).__name__}")
    if not 1 <= value <= 5:
        raise InvalidPriorityError(f"Priority must be between 1 and 5, got {value}")
    return value


def validate_status(value: Any) -> str:
    allowed = ("pending", "in_progress", "completed", "cancelled")
    if not isinstance(value, str):
        raise InvalidStatusError(f"Status must be str, got {type(value).__name__}")
    if value not in allowed:
        raise InvalidStatusError(f"Status must be one of {allowed}, got '{value}'")
    return value


def validate_created_at(value: Any) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"created_at must be datetime, got {type(value).__name__}")
    return value