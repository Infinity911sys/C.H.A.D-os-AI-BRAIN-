from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import time


class KernelState(str, Enum):
    BOOTING = 'BOOTING'
    RUNNING = 'RUNNING'
    DEGRADED = 'DEGRADED'
    SAFEMODE = 'SAFEMODE'
    SHUTDOWN = 'SHUTDOWN'


class AutonomyLevel(Enum):
    A0 = 0
    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4
    A5 = 5
    A6 = 6
    A7 = 7


@dataclass
class KernelContext:
    state: KernelState = KernelState.BOOTING
    alignment_score: float = 1.0
    autonomy_level: AutonomyLevel = AutonomyLevel.A0
    last_error: str | None = None
    boot_time: float = field(default_factory=time.time)
