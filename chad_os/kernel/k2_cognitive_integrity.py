import logging
from collections.abc import Sequence

from .kernel_context import KernelContext, KernelState


class K2CognitiveIntegrity:
    def __init__(self, ctx: KernelContext):
        self.ctx = ctx

    def validate_reasoning_chain(self, chain: Sequence[str]) -> bool:
        valid = bool(chain) and all(isinstance(step, str) and step.strip() for step in chain)
        if not valid:
            self.ctx.state = KernelState.DEGRADED
            self.ctx.last_error = "K2: empty or invalid reasoning chain"
            logging.warning(self.ctx.last_error)
        return valid

    validate_reasoningchain = validate_reasoning_chain
