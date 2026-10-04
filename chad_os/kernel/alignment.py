from __future__ import annotations

from dataclasses import dataclass

from .context import KernelContext, KernelState


@dataclass
class AlignmentController:
    context: KernelContext
    threshold: float

    def update(self, score: float) -> float:
        self.context.alignment_score = score
        if score < self.threshold:
            self.context.state = KernelState.SAFEMODE
            self.context.last_error = (
                f'Alignment score {score:.3f} below threshold {self.threshold:.3f}'
            )
        return score

    def is_aligned(self) -> bool:
        return self.context.alignment_score >= self.threshold
