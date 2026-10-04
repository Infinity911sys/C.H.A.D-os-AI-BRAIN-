from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class TelemetryAggregator:
    events: list[dict[str, Any]] = field(default_factory=list)
    source_counts: Counter = field(default_factory=Counter)

    def ingest(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = {
            'source': payload.get('source', 'unknown'),
            'event_type': payload.get('event_type', 'telemetry'),
            'severity': int(payload.get('severity', 1)),
            'location': payload.get('location'),
            'payload': payload.get('payload', {}),
            'timestamp': payload.get('timestamp', time.time()),
        }
        self.events.append(normalized)
        self.source_counts[normalized['source']] += 1
        return normalized

    def summary(self) -> dict[str, Any]:
        return {
            'total_events': len(self.events),
            'sources': dict(self.source_counts),
            'latest_event': self.events[-1] if self.events else None,
        }
