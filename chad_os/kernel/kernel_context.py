import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class KernelState(Enum):
    BOOTING = "booting"
    RUNNING = "running"
    SAFEMODE = "safemode"
    SHUTDOWN = "shutdown"
    DEGRADED = "degraded"


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
    autonomy_level: AutonomyLevel = AutonomyLevel.A0
    alignment_score: float = 1.0
    collective_coherence: float = 1.0
    last_error: Optional[str] = None
    boot_time: float = field(default_factory=time.time)


class KernelViolation(Exception):
    """Raised when a kernel-level constraint is violated."""
