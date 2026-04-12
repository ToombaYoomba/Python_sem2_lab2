from datetime import datetime
from typing import Optional

from src.domain.descriptors import (
    ValidatedAttribute,
    CachedProperty,
    validate_task_id,
    validate_description,
    validate_priority,
    validate_status,
    validate_created_at,
)
from src.domain.exceptions import InvalidStatusError
from src.contracts.message import Message


class Task:
    id = ValidatedAttribute("id", validate_task_id, immutable=True)
    description = ValidatedAttribute("description", validate_description)
    priority = ValidatedAttribute("priority", validate_priority)
    status = ValidatedAttribute("status", validate_status)
    created_at = ValidatedAttribute("created_at", validate_created_at, immutable=True)

    def __init__(
        self,
        task_id: str,
        description: str,
        priority: int = 3,
        status: str = "pending",
        created_at: Optional[datetime] = None,
    ):
        self.id = task_id
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()

    @property
    def is_ready(self) -> bool:
        return self.status in ("pending", "in_progress") and self.priority >= 2

    @property
    def is_blocked(self) -> bool:
        return self.status == "cancelled"

    @property
    def age_hours(self) -> float:
        delta = datetime.now() - self.created_at
        return delta.total_seconds() / 3600

    @CachedProperty
    def urgency_score(self) -> float:
        priority_weight = self.priority * 10
        status_weight = {"pending": 5, "in_progress": 3, "completed": 0, "cancelled": 0}
        base_score = priority_weight + status_weight.get(self.status, 0)
        time_factor = max(0, 100 - self.age_hours * 2)
        return base_score + time_factor

    def complete(self) -> None:
        if self.status == "cancelled":
            raise InvalidStatusError("Cannot complete a cancelled task")
        self.status = "completed"

    def start(self) -> None:
        if self.status == "completed":
            raise InvalidStatusError("Cannot start a completed task")
        if self.status == "cancelled":
            raise InvalidStatusError("Cannot start a cancelled task")
        self.status = "in_progress"

    def cancel(self) -> None:
        if self.status == "completed":
            raise InvalidStatusError("Cannot cancel a completed task")
        self.status = "cancelled"

    @classmethod
    def from_message(cls, message: Message, priority: int = 3) -> "Task":
        return cls(
            task_id=message.id,
            description=f"{message.title}: {message.message}",
            priority=priority,
        )

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, description={self.description[:50]!r}, "
            f"priority={self.priority}, status={self.status!r})"
        )