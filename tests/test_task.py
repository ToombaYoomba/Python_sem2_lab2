import pytest
from datetime import datetime
from src.domain.task import Task
from src.domain.exceptions import (
    InvalidTaskIdError, InvalidPriorityError,
    InvalidStatusError, InvalidDescriptionError,
    ImmutableAttributeError
)
from src.contracts.message import Message


class TestTaskValidation:
    def test_valid_task_creation(self):
        task = Task(task_id="t1", description="Valid description", priority=3)
        assert task.id == "t1"
        assert task.description == "Valid description"
        assert task.priority == 3
        assert task.status == "pending"

    def test_invalid_task_id(self):
        with pytest.raises(InvalidTaskIdError):
            Task(task_id="", description="desc")

        with pytest.raises(InvalidTaskIdError):
            Task(task_id=123, description="desc")

    def test_invalid_description(self):
        with pytest.raises(InvalidDescriptionError):
            Task(task_id="t1", description="ab")

        with pytest.raises(InvalidDescriptionError):
            Task(task_id="t1", description=123)

    def test_invalid_priority(self):
        with pytest.raises(InvalidPriorityError):
            Task(task_id="t1", description="desc", priority=0)

        with pytest.raises(InvalidPriorityError):
            Task(task_id="t1", description="desc", priority=6)

    def test_immutable_id(self):
        task = Task(task_id="t1", description="desc")
        with pytest.raises(ImmutableAttributeError):
            task.id = "t2"

    def test_immutable_created_at(self):
        task = Task(task_id="t1", description="desc")
        with pytest.raises(ImmutableAttributeError):
            task.created_at = datetime.now()


class TestTaskStateTransitions:
    def test_complete_pending(self):
        task = Task(task_id="t1", description="desc")
        task.complete()
        assert task.status == "completed"

    def test_cannot_complete_cancelled(self):
        task = Task(task_id="t1", description="desc")
        task.cancel()
        with pytest.raises(InvalidStatusError):
            task.complete()

    def test_cannot_start_completed(self):
        task = Task(task_id="t1", description="desc")
        task.complete()
        with pytest.raises(InvalidStatusError):
            task.start()

    def test_cannot_start_cancelled(self):
        task = Task(task_id="t1", description="desc")
        task.cancel()
        with pytest.raises(InvalidStatusError):
            task.start()


class TestTaskProperties:
    def test_is_ready(self):
        task = Task(task_id="t1", description="desc", priority=2)
        assert task.is_ready is True

        task = Task(task_id="t1", description="desc", priority=1)
        assert task.is_ready is False

    def test_urgency_score_caching(self):
        task = Task(task_id="t1", description="desc")
        score1 = task.urgency_score
        score2 = task.urgency_score
        assert score1 == score2

    def test_factory_from_message(self):
        msg = Message(id="m1", title="Test", author="Author", message="Content")
        task = Task.from_message(msg, priority=4)
        assert task.id == "m1"
        assert "Test: Content" in task.description
        assert task.priority == 4