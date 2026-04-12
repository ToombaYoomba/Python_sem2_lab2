import pytest
from src.inbox.core import InboxApp


def test_with_no_sources():
    inbox = InboxApp([])
    assert list(inbox.iter_messages()) == []


def test_with_one_source(sample_messages):
    class Source:
        name = "test"
        def fetch(self):
            return iter(sample_messages)

    inbox = InboxApp([Source()])
    messages = list(inbox.iter_messages())
    assert len(messages) == 2
    assert messages[0].id == "1"
    assert messages[1].id == "2"


def test_with_multiple_sources(sample_messages):
    class SourceA:
        name = "A"
        def fetch(self):
            return iter([sample_messages[0]])

    class SourceB:
        name = "B"
        def fetch(self):
            return iter([sample_messages[1]])

    inbox = InboxApp([SourceA(), SourceB()])
    messages = list(inbox.iter_messages())
    assert len(messages) == 2


def test_rejects_invalid_source(invalid_source):
    inbox = InboxApp([invalid_source])
    with pytest.raises(TypeError, match="does not implement MessageSource protocol"):
        list(inbox.iter_messages())


def test_yields_lazily():
    class LazySource:
        name = "lazy"
        def fetch(self):
            yield 1
            yield 2

    inbox = InboxApp([LazySource()])
    iterator = inbox.iter_messages()
    assert next(iterator) == 1
    assert next(iterator) == 2