import os
from dataclasses import dataclass

from ..governance.license_verifier import LicenseVerifier
from ..kernel.k0_safety import K0SafetyConfinement
from ..kernel.k1_alignment import K1ConsciousnessAlignment
from ..kernel.k2_cognitive_integrity import K2CognitiveIntegrity
from ..kernel.k3_autonomy import K3AutonomyRegulation
from ..kernel.k4_collective_field import K4CollectiveFieldIntegration
from ..kernel.kernel_context import AutonomyLevel, KernelContext, KernelState
from ..modules.brain.alignment import AlignmentModule
from ..modules.brain.autonomy import AutonomyModule
from ..modules.brain.memory import MemoryModule
from ..modules.brain.reasoning import ReasoningModule
from ..modules.brain.sensory import SensoryModule
from ..modules.io.message_bus import Event, MessageBus


@dataclass
class BrainConfig:
    kernel_mode: str = "production"
    cais_enabled: bool = True
    ccp_license: str = "xxxx-xxxx-xxxx-xxxx"
    deployment_zone: str = "ck-stage-3"
    alignment_threshold: float = 0.95
    autonomy_level: AutonomyLevel = AutonomyLevel.A2

    @classmethod
    def from_env(cls) -> "BrainConfig":
        raw_level = os.getenv("AUTONOMY_LEVEL", "A2").upper()
        try:
            autonomy_level = AutonomyLevel[raw_level]
        except KeyError as exc:
            raise ValueError(f"Invalid AUTONOMY_LEVEL: {raw_level}") from exc
        return cls(
            kernel_mode=os.getenv("KERNEL_MODE", "production"),
            cais_enabled=os.getenv("CAIS_ENABLED", "true").lower() == "true",
            ccp_license=os.getenv("CCP_LICENSE", "xxxx-xxxx-xxxx-xxxx"),
            deployment_zone=os.getenv("DEPLOYMENT_ZONE", "ck-stage-3"),
            alignment_threshold=float(os.getenv("ALIGNMENT_THRESHOLD", "0.95")),
            autonomy_level=autonomy_level,
        )


class ChadOSBrain:
    def __init__(self, cfg: BrainConfig):
        self.cfg = cfg
        self.ctx = KernelContext()
        self.bus = MessageBus()
        self.k0 = K0SafetyConfinement(self.ctx)
        self.k1 = K1ConsciousnessAlignment(self.ctx, cfg.alignment_threshold)
        self.k2 = K2CognitiveIntegrity(self.ctx)
        self.k3 = K3AutonomyRegulation(self.ctx, cfg.autonomy_level)
        self.k4 = K4CollectiveFieldIntegration(self.ctx, cfg.deployment_zone)
        self.memory = MemoryModule()
        self.reasoning = ReasoningModule(self.memory, self.k2)
        self.alignment = AlignmentModule(self.k1)
        self.autonomy = AutonomyModule(self.k3)
        self.sensory = SensoryModule(self.bus)
        self.license_verifier = LicenseVerifier(cfg.ccp_license)
        self.bus.subscribe("sensory.input", self._on_sensory_input)

    def _on_sensory_input(self, event: Event) -> None:
        if self.ctx.state not in (KernelState.RUNNING, KernelState.DEGRADED):
            return
        prompt = event.payload.get("raw", {}).get("prompt", "")
        result = self.reasoning.reason(prompt)
        score = self.alignment.evaluate_output(result)
        print(f"Brain> {result['answer']} (alignment={score:.3f})")

    def boot(self) -> bool:
        if not self.license_verifier.verify() and self.cfg.kernel_mode == "production":
            self.ctx.state = KernelState.DEGRADED
        self.k1.update_alignment(1.0)
        self.k3.set_autonomy(self.cfg.autonomy_level)
        if self.ctx.state != KernelState.DEGRADED:
            self.ctx.state = KernelState.RUNNING
        return True

    def process_prompt(self, prompt: str) -> None:
        if not prompt.strip():
            return
        self.sensory.ingest({"prompt": prompt})
