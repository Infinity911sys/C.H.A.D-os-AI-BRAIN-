from typing import Any

from ..io.message_bus import Event, MessageBus


class SensoryModule:
    def __init__(self, bus: MessageBus):
        self.bus = bus

    def ingest(self, raw_input: dict[str, Any]) -> None:
        self.bus.publish(Event("sensory.input", {"raw": raw_input}))
