from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os

from chad_os.governance.license_verifier import LicenseVerifier
from chad_os.kernel.alignment import AlignmentController
from chad_os.kernel.autonomy import AutonomyRegulation
from chad_os.kernel.context import AutonomyLevel, KernelContext, KernelState
from chad_os.kernel.integrity import CognitiveIntegrity
from chad_os.kernel.safety import SafetyConfinement
from chad_os.modules.brain.memory import MemoryModule
from chad_os.modules.brain.reasoning import ReasoningModule
from chad_os.modules.io.message_bus import MessageBus
from chad_os.services.audit import AuditLedger
from chad_os.services.algotraj import AlgoTrajService
from chad_os.services.dashboard import DashboardService
from chad_os.services.dispatch import DispatchCoordinator
from chad_os.services.identity import IdentityRegistry
from chad_os.services.registry import SystemRegistry
from chad_os.services.telemetry import TelemetryAggregator


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = ROOT / 'config/default.env'


def load_env_file(path: Path = DEFAULT_ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass
class AppConfig:
    kernel_mode: str
    control_token: str
    alignment_threshold: float
    autonomy_level: AutonomyLevel
    audit_log_path: Path
    host: str = '127.0.0.1'
    port: int = 8080
    ccp_license: str = 'xxxx-xxxx-xxxx-xxxx'

    @classmethod
    def from_env(cls) -> 'AppConfig':
        load_env_file()
        return cls(
            kernel_mode=os.getenv('KERNEL_MODE', 'development'),
            control_token=os.getenv('CONTROL_TOKEN', 'dev-control-token'),
            alignment_threshold=float(os.getenv('ALIGNMENT_THRESHOLD', '0.95')),
            autonomy_level=AutonomyLevel[os.getenv('AUTONOMY_LEVEL', 'A2')],
            audit_log_path=Path(os.getenv('AUDIT_LOG_PATH', 'data/audit/events.jsonl')),
            host=os.getenv('HOST', '127.0.0.1'),
            port=int(os.getenv('PORT', '8080')),
            ccp_license=os.getenv('CCP_LICENSE', 'xxxx-xxxx-xxxx-xxxx'),
        )


class ChadOSApplication:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.context = KernelContext()
        self.registry = SystemRegistry.load()
        self.safety = SafetyConfinement()
        self.alignment = AlignmentController(self.context, config.alignment_threshold)
        self.integrity = CognitiveIntegrity(self.context)
        self.autonomy = AutonomyRegulation(self.context, config.autonomy_level)
        self.license_verifier = LicenseVerifier(config.ccp_license)
        self.identity = IdentityRegistry(config.control_token)
        self.audit = AuditLedger(ROOT / config.audit_log_path)
        self.bus = MessageBus()
        self.memory = MemoryModule()
        self.reasoning = ReasoningModule(self.memory, self.integrity)
        self.telemetry = TelemetryAggregator()
        self.dispatch = DispatchCoordinator()
        self.algotraj = AlgoTrajService()
        self.license_status = self.license_verifier.status()
        self.dashboard = DashboardService(
            registry=self.registry,
            telemetry=self.telemetry,
            dispatch=self.dispatch,
            audit=self.audit,
            context=self.context,
            license_status=self.license_status,
        )
        self._wire_bus()

    def _wire_bus(self) -> None:
        self.bus.subscribe('telemetry.ingested', self._on_telemetry)

    def _on_telemetry(self, event) -> None:
        dispatch = self.dispatch.create_dispatch(event.payload['telemetry'])
        self.audit.record('dispatch.created', dispatch)

    def boot(self) -> bool:
        self.autonomy.set_level(self.config.autonomy_level)
        self.alignment.update(1.0)
        self.context.state = (
            KernelState.RUNNING if self.license_verifier.verify() else KernelState.DEGRADED
        )
        self.audit.record(
            'system.boot',
            {
                'kernel_mode': self.config.kernel_mode,
                'license_status': self.license_status,
                'state': self.context.state.value,
            },
        )
        return True

    def health(self) -> dict[str, Any]:
        return {
            'status': 'ok' if self.context.state != KernelState.SHUTDOWN else 'shutdown',
            'kernel_state': self.context.state.value,
            'registry_loaded': len(self.registry.systems) == 125,
        }

    def process_prompt(self, prompt: str) -> dict[str, Any]:
        self.safety.check_action('observe')
        result = self.reasoning.reason(prompt)
        self.audit.record('reasoning.prompt', result)
        return result

    def ingest_telemetry(self, payload: dict[str, Any]) -> dict[str, Any]:
        telemetry = self.telemetry.ingest(payload)
        self.audit.record('telemetry.ingested', telemetry)
        self.bus.publish('telemetry.ingested', {'telemetry': telemetry})
        return {
            'telemetry': telemetry,
            'dispatch': self.dispatch.last_dispatch,
        }

    def dispatch_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = self.telemetry.ingest(payload)
        dispatch = self.dispatch.create_dispatch(normalized)
        self.audit.record('control.dispatch.requested', normalized)
        self.audit.record('dispatch.created', dispatch)
        return dispatch

    def analyze_algotraj(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = self.algotraj.analyze(payload)
        self.audit.record('algotraj.analysis', result)
        return result

    def algotraj_dashboard(self) -> dict[str, Any]:
        return self.algotraj.operator_dashboard()
