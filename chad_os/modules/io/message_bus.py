import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Event:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MessageBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        for handler in tuple(self._subscribers.get(event.type, ())):
            try:
                handler(event)
            except Exception:
                logging.exception("Error handling event %s", event.type)
