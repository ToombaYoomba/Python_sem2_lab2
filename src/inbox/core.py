from collections.abc import Sequence, Iterable
from typing import Optional

from src.contracts.message import Message
from src.contracts.message_source import MessageSource
from src.domain.task import Task


class InboxApp:
    def __init__(self, sources: Optional[Sequence[MessageSource]] = None):
        self._sources = sources or []

    def iter_messages(self) -> Iterable[Message]:
        for src in self._sources:
            if not isinstance(src, MessageSource):
                raise TypeError(
                    f"Source object of type {type(src).__name__} does not implement MessageSource protocol"
                )
            for message in src.fetch():
                yield message

    def iter_tasks(self, default_priority: int = 3) -> Iterable[Task]:
        for message in self.iter_messages():
            yield Task.from_message(message, priority=default_priority)