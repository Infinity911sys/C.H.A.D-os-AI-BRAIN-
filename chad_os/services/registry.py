from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
from urllib.parse import parse_qs


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

    def sections(self) -> list[dict[str, Any]]:
        ordered: dict[str, dict[str, Any]] = {}
        for system in self.systems:
            section = system['section']
            if section not in ordered:
                ordered[section] = {
                    'section': section,
                    'section_name': system['section_name'],
                    'count': 0,
                }
            ordered[section]['count'] += 1
        return list(ordered.values())

    def public_catalog(
        self,
        *,
        search: str = '',
        section: str = '',
        operational_status: str = '',
        asset_class: str = '',
        limit: int | None = None,
    ) -> dict[str, Any]:
        items = self.systems

        if search:
            needle = search.lower()
            items = [
                system
                for system in items
                if needle in system['id'].lower()
                or needle in system['name'].lower()
                or needle in system['purpose'].lower()
                or needle in system['section_name'].lower()
            ]
        if section:
            items = [system for system in items if system['section'] == section]
        if operational_status:
            items = [
                system
                for system in items
                if system['operational_status'] == operational_status
            ]
        if asset_class:
            items = [system for system in items if system['asset_class'] == asset_class]

        if limit is not None:
            items = items[:limit]

        return {
            'metadata': self.metadata,
            'filters': {
                'search': search,
                'section': section,
                'operational_status': operational_status,
                'asset_class': asset_class,
                'limit': limit,
            },
            'sections': self.sections(),
            'count': len(items),
            'systems': items,
        }

    def public_payload(self) -> dict[str, Any]:
        return {
            'metadata': self.metadata,
            'summary': self.summary(),
            'sections': self.sections(),
            'core_systems': self.core_systems(),
        }

    @staticmethod
    def filters_from_query(query: str) -> dict[str, Any]:
        params = parse_qs(query, keep_blank_values=False)

        def first(name: str) -> str:
            return params.get(name, [''])[0].strip()

        limit_value = first('limit')
        limit = int(limit_value) if limit_value.isdigit() else None
        return {
            'search': first('search'),
            'section': first('section'),
            'operational_status': first('status'),
            'asset_class': first('asset_class'),
            'limit': limit,
        }
