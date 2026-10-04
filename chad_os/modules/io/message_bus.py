from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable
import time


@dataclass
class Event:
    topic: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class MessageBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: dict[str, Any]) -> Event:
        event = Event(topic=topic, payload=payload)
        for handler in self._subscribers.get(topic, []):
            handler(event)
        return event
