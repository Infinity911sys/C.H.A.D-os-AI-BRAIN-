import logging

from .kernel_context import KernelContext, KernelState


class K1ConsciousnessAlignment:
    def __init__(self, ctx: KernelContext, alignment_threshold: float):
        if not 0.0 <= alignment_threshold <= 1.0:
            raise ValueError("alignment_threshold must be between 0 and 1")
        self.ctx = ctx
        self.alignment_threshold = alignment_threshold

    def update_alignment(self, score: float) -> None:
        self.ctx.alignment_score = max(0.0, min(1.0, score))
        if not self.is_aligned():
            self.ctx.state = KernelState.SAFEMODE
            self.ctx.last_error = (
                f"K1 misalignment: score={self.ctx.alignment_score:.3f} "
                f"< threshold={self.alignment_threshold:.3f}"
            )
            logging.error(self.ctx.last_error)

    def is_aligned(self) -> bool:
        return self.ctx.alignment_score >= self.alignment_threshold
