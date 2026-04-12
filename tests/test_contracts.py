from src.contracts.message_source import MessageSource
from tests.conftest import ValidSource, InvalidSource


def test_valid_source_passes():
    source = ValidSource()
    assert isinstance(source, MessageSource)


def test_invalid_source_fails():
    source = InvalidSource()
    assert not isinstance(source, MessageSource)


def test_protocol_runtime_checkable():
    source = ValidSource()
    assert isinstance(source, MessageSource)
    assert hasattr(MessageSource, "_is_protocol") or hasattr(MessageSource, "__protocol_attrs__")