import io
import pytest
from src.sources.stdin import StdinLineSource, create_source


def test_reads_valid_lines():
    input_data = io.StringIO("1:Hello:Alice:Test\n2:World:Bob:Another\n")
    source = StdinLineSource(stream=input_data)
    messages = list(source.fetch())
    assert len(messages) == 2
    assert messages[0].id == "1"
    assert messages[0].title == "Hello"
    assert messages[0].author == "Alice"
    assert messages[0].message.rstrip('\n') == "Test"
    assert messages[1].id == "2"
    assert messages[1].title == "World"
    assert messages[1].author == "Bob"
    assert messages[1].message.rstrip('\n') == "Another"


def test_skips_empty_lines():
    input_data = io.StringIO("1:Hello:Alice:Test\n\n2:World:Bob:Another\n\n")
    source = StdinLineSource(stream=input_data)
    messages = list(source.fetch())
    assert len(messages) == 2


def test_handles_extra_fields():
    input_data = io.StringIO("1:Hello:Alice:Test:Extra:Ignored\n")
    source = StdinLineSource(stream=input_data)
    messages = list(source.fetch())
    assert messages[0].message == "Test"


def test_raises_on_insufficient_fields():
    input_data = io.StringIO("1:Hello:Alice\n")
    source = StdinLineSource(stream=input_data)
    with pytest.raises(ValueError, match="Message must contain at least 4 items"):
        list(source.fetch())


def test_has_correct_name():
    input_data = io.StringIO("1:Test:Author:Msg")
    source = StdinLineSource(stream=input_data)
    assert source.name == "stdin"


def test_create_source_factory():
    source = create_source()
    assert isinstance(source, StdinLineSource)