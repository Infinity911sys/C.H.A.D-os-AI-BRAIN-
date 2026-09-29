import logging

from .kernel_context import AutonomyLevel, KernelContext, KernelViolation


class K3AutonomyRegulation:
    def __init__(self, ctx: KernelContext, max_autonomy: AutonomyLevel):
        self.ctx = ctx
        self.max_autonomy = max_autonomy

    def set_autonomy(self, level: AutonomyLevel) -> None:
        if level.value > self.max_autonomy.value:
            message = f"K3: attempted autonomy {level.name} > allowed {self.max_autonomy.name}"
            self.ctx.last_error = message
            logging.error(message)
            raise KernelViolation(message)
        self.ctx.autonomy_level = level
