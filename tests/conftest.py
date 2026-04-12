import pytest

from src.contracts.message import Message


@pytest.fixture
def sample_message():
    return Message(id="1", title="Test", author="Tester", message="Hello")


@pytest.fixture
def sample_messages():
    return [
        Message(id="1", title="A", author="A1", message="Msg1"),
        Message(id="2", title="B", author="B1", message="Msg2"),
    ]


@pytest.fixture
def valid_jsonl_file(tmp_path):
    content = (
        '{"id": "1", "title": "Hello", "author": "Alice", "message": "First"}\n'
        '{"id": "2", "title": "World", "author": "Bob", "message": "Second"}\n'
    )
    file = tmp_path / "test.jsonl"
    file.write_text(content, encoding="utf-8")
    return file


@pytest.fixture
def empty_jsonl_file(tmp_path):
    file = tmp_path / "empty.jsonl"
    file.write_text("", encoding="utf-8")
    return file


class ValidSource:
    name = "test"
    def fetch(self):
        yield Message(id="t1", title="T", author="A", message="M")


class InvalidSource:
    name = "invalid"


@pytest.fixture
def valid_source():
    return ValidSource()


@pytest.fixture
def invalid_source():
    return InvalidSource()