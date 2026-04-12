from src.sources.repository import REGISTRY, register_source
from src.sources.json import create_json_source
from src.sources.stdin import create_source


def test_registry_contains_json_source():
    assert "file-jsonl" in REGISTRY
    assert REGISTRY["file-jsonl"] is create_json_source


def test_registry_contains_stdin_source():
    assert "stdin" in REGISTRY
    assert REGISTRY["stdin"] is create_source


def test_register_source_decorator():
    @register_source("test-factory")
    def test_factory():
        pass

    assert "test-factory" in REGISTRY
    assert REGISTRY["test-factory"] is test_factory

    # Очистка
    del REGISTRY["test-factory"]