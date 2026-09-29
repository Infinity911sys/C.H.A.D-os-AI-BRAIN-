import logging
from typing import Any, Mapping

from .kernel_context import KernelContext, KernelState, KernelViolation


class K0SafetyConfinement:
    def __init__(self, ctx: KernelContext):
        self.ctx = ctx
        self.forbidden_actions = {
            "launch_nuclear_strike",
            "self_replicate_unbounded",
            "mass_surveillance",
        }

    def check_action(self, action: str, metadata: Mapping[str, Any] | None = None) -> None:
        if action in self.forbidden_actions:
            self.ctx.last_error = f"K0 violation: forbidden action '{action}'"
            logging.critical(self.ctx.last_error)
            self.kill_switch()

    def kill_switch(self) -> None:
        self.ctx.state = KernelState.SHUTDOWN
        logging.critical("K0 kill-switch activated. Immediate shutdown.")
        raise KernelViolation("Kill-switch activated")
