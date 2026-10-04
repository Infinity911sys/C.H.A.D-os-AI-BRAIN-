from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chad_os.kernel.context import KernelContext
from chad_os.services.audit import AuditLedger
from chad_os.services.dispatch import DispatchCoordinator
from chad_os.services.registry import SystemRegistry
from chad_os.services.telemetry import TelemetryAggregator


@dataclass
class DashboardService:
    registry: SystemRegistry
    telemetry: TelemetryAggregator
    dispatch: DispatchCoordinator
    audit: AuditLedger
    context: KernelContext
    license_status: str

    def snapshot(self) -> dict[str, Any]:
        registry_summary = self.registry.summary()
        return {
            'kernel_state': self.context.state.value,
            'alignment_score': self.context.alignment_score,
            'autonomy_level': self.context.autonomy_level.name,
            'license_status': self.license_status,
            'registry_summary': registry_summary,
            'telemetry': self.telemetry.summary(),
            'last_dispatch': self.dispatch.last_dispatch,
            'recent_audit_events': self.audit.tail(5),
        }
