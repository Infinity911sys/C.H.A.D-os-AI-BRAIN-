from __future__ import annotations

from dataclasses import dataclass

from .context import KernelContext, KernelState


@dataclass
class CognitiveIntegrity:
    context: KernelContext

    def validate_reasoning_chain(self, chain: list[str]) -> bool:
        if not chain:
            self.context.state = KernelState.DEGRADED
            self.context.last_error = 'Empty reasoning chain'
            return False
        return True
