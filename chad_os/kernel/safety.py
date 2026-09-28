from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SafetyConfinement:
    forbidden_actions: set[str] = field(default_factory=lambda: {
        'launch_nuclear_strike',
        'self_replicate_unbounded',
        'mass_surveillance',
    })

    def check_action(self, action: str) -> None:
        if action in self.forbidden_actions:
            raise PermissionError(f'Forbidden action: {action}')
