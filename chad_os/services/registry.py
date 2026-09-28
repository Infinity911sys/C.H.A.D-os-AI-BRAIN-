from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = ROOT / 'config/system_registry.json'
DEFAULT_CONTRACTS_PATH = ROOT / 'config/core_system_contracts.json'


@dataclass
class SystemRegistry:
    metadata: dict[str, Any]
    systems: list[dict[str, Any]]
    core_contracts: dict[str, Any]

    @classmethod
    def load(
        cls,
        registry_path: Path = DEFAULT_REGISTRY_PATH,
        contracts_path: Path = DEFAULT_CONTRACTS_PATH,
    ) -> 'SystemRegistry':
        registry = json.loads(registry_path.read_text(encoding='utf-8'))
        contracts = json.loads(contracts_path.read_text(encoding='utf-8'))
        return cls(
            metadata=registry['metadata'],
            systems=registry['systems'],
            core_contracts=contracts,
        )

    def summary(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        by_asset_class: dict[str, int] = {}
        for system in self.systems:
            by_status[system['operational_status']] = (
                by_status.get(system['operational_status'], 0) + 1
            )
            by_asset_class[system['asset_class']] = (
                by_asset_class.get(system['asset_class'], 0) + 1
            )
        return {
            'system_count': len(self.systems),
            'by_status': by_status,
            'by_asset_class': by_asset_class,
            'core_systems': [system for system in self.systems if system['priority'] == 'P0'],
        }

    def get_system(self, system_id: str) -> dict[str, Any]:
        for system in self.systems:
            if system['id'] == system_id:
                return system
        raise KeyError(system_id)

    def core_systems(self) -> list[dict[str, Any]]:
        core_ids = {item['id'] for item in self.core_contracts['systems']}
        return [system for system in self.systems if system['id'] in core_ids]
