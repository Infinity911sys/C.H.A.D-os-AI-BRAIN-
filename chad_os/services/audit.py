from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any
import json
import time


@dataclass
class AuditLedger:
    path: Path

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def record(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'payload': payload,
        }
        with self._lock:
            with self.path.open('a', encoding='utf-8') as handle:
                handle.write(json.dumps(event, sort_keys=True) + '
')
        return event

    def tail(self, limit: int = 10) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding='utf-8').splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
