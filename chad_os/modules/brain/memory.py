from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryModule:
    recent: list[dict[str, Any]] = field(default_factory=list)
    limit: int = 100

    def store(self, item: dict[str, Any]) -> None:
        self.recent.append(item)
        if len(self.recent) > self.limit:
            self.recent.pop(0)

    def tail(self, size: int = 5) -> list[dict[str, Any]]:
        return self.recent[-size:]
