from ...kernel.k3_autonomy import K3AutonomyRegulation
from ...kernel.kernel_context import AutonomyLevel, KernelViolation


class AutonomyModule:
    def __init__(self, k3: K3AutonomyRegulation):
        self.k3 = k3

    def request_autonomy(self, level: AutonomyLevel) -> bool:
        try:
            self.k3.set_autonomy(level)
        except KernelViolation:
            return False
        return True
