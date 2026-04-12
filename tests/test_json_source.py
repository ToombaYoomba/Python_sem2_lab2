import pytest
from pathlib import Path
from src.sources.json import JsonlSource, create_json_source


def test_reads_valid_file(valid_jsonl_file):
    source = JsonlSource(valid_jsonl_file)
    messages = list(source.fetch())
    assert len(messages) == 2
    assert messages[0].id == "1"
    assert messages[0].title == "Hello"
    assert messages[1].message == "Second"


def test_skips_empty_lines(tmp_path):
    content = (
        '{"id": "1", "title": "A", "author": "B", "message": "C"}\n'
        "\n"
        '{"id": "2", "title": "D", "author": "E", "message": "F"}\n'
    )
    file = tmp_path / "test.jsonl"
    file.write_text(content)

    source = JsonlSource(file)
    messages = list(source.fetch())
    assert len(messages) == 2


def test_handles_missing_fields(tmp_path):
    content = '{"id": "1"}\n{"title": "No ID", "author": "X", "message": "Msg"}\n'
    file = tmp_path / "test.jsonl"
    file.write_text(content)

    source = JsonlSource(file)
    messages = list(source.fetch())

    assert messages[0].title == ""
    assert messages[0].message == ""
    assert messages[1].id == f"{file.name}:2"


def test_raises_on_invalid_json(tmp_path):
    content = '{"id": "1", "title": "Bad"  # missing brace\n'
    file = tmp_path / "invalid.jsonl"
    file.write_text(content)

    source = JsonlSource(file)
    with pytest.raises(ValueError, match="Bad JSON"):
        list(source.fetch())


def test_has_correct_name(valid_jsonl_file):
    source = JsonlSource(valid_jsonl_file)
    assert source.name == "file-jsonl"


def test_create_factory(valid_jsonl_file):
    source = create_json_source(valid_jsonl_file)
    assert isinstance(source, JsonlSource)