from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import time


SEVERITY_TO_PRIORITY = {
    1: 'monitor',
    2: 'routine',
    3: 'priority',
    4: 'urgent',
    5: 'critical',
}


@dataclass
class DispatchCoordinator:
    last_dispatch: dict[str, Any] | None = None
    history: list[dict[str, Any]] = field(default_factory=list)

    def create_dispatch(self, telemetry_event: dict[str, Any]) -> dict[str, Any]:
        severity = max(1, min(int(telemetry_event.get('severity', 1)), 5))
        priority = SEVERITY_TO_PRIORITY[severity]
        response_mode = 'escalate' if severity >= 4 else 'coordinate'
        route = 'Infinity911' if severity >= 3 else 'Resource Finder Engine'
        dispatch = {
            'created_at': time.time(),
            'source': telemetry_event.get('source', 'unknown'),
            'priority': priority,
            'response_mode': response_mode,
            'route': route,
            'recommended_unit': (
                'Autonomous Dispatch Coordinator' if severity >= 4 else 'AE Command'
            ),
            'location': telemetry_event.get('location'),
            'telemetry_event': telemetry_event,
        }
        self.last_dispatch = dispatch
        self.history.append(dispatch)
        return dispatch
