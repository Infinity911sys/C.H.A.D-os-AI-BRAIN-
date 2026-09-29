from chad_os.kernel.kernel_context import AutonomyLevel, KernelContext, KernelState
from chad_os.kernel.k2_cognitive_integrity import K2CognitiveIntegrity
from chad_os.modules.brain.memory import MemoryModule
from chad_os.modules.brain.reasoning import ReasoningModule
from chad_os.runtime.bootstrap import BrainConfig, ChadOSBrain


def test_reasoning_basic():
    result = ReasoningModule(MemoryModule(), K2CognitiveIntegrity(KernelContext())).reason("hello")
    assert result["valid"] is True
    assert "Stub answer" in result["answer"]


def test_development_boot_allows_placeholder_license():
    brain = ChadOSBrain(BrainConfig(kernel_mode="development"))
    assert brain.boot() is True
    assert brain.ctx.state is KernelState.RUNNING
    assert brain.ctx.autonomy_level is AutonomyLevel.A2


def test_production_placeholder_license_degrades():
    brain = ChadOSBrain(BrainConfig())
    brain.boot()
    assert brain.ctx.state is KernelState.DEGRADED
