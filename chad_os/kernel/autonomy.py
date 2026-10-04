from __future__ import annotations

from dataclasses import dataclass

from .context import AutonomyLevel, KernelContext


@dataclass
class AutonomyRegulation:
    context: KernelContext
    max_level: AutonomyLevel

    def set_level(self, level: AutonomyLevel) -> None:
        if level.value > self.max_level.value:
            raise PermissionError(
                f'Autonomy {level.name} exceeds configured ceiling {self.max_level.name}'
            )
        self.context.autonomy_level = level
