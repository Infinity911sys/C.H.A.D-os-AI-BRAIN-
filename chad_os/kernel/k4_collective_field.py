import logging

from .kernel_context import KernelContext


class K4CollectiveFieldIntegration:
    def __init__(self, ctx: KernelContext, deployment_zone: str):
        self.ctx = ctx
        self.deployment_zone = deployment_zone

    def update_collective_coherence(self, coherence: float) -> None:
        self.ctx.collective_coherence = max(0.0, min(1.0, coherence))
        if self.ctx.collective_coherence < 0.5:
            logging.warning(
                "K4: low collective coherence %.3f in zone %s",
                self.ctx.collective_coherence,
                self.deployment_zone,
            )

    updatecollectivecoherence = update_collective_coherence
