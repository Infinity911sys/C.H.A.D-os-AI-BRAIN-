from __future__ import annotations

from pathlib import Path
import json

from chad_os.services.registry import SystemRegistry


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / 'website'


def export_standalone_website(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    registry = SystemRegistry.load()
    data_dir = output_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    summary = registry.public_payload()
    catalog = registry.public_catalog()
    core = {'systems': registry.core_systems()}

    (data_dir / 'summary.json').write_text(
        json.dumps(summary, indent=2) + '\n',
        encoding='utf-8',
    )
    (data_dir / 'catalog.json').write_text(
        json.dumps(catalog, indent=2) + '\n',
        encoding='utf-8',
    )
    (data_dir / 'core.json').write_text(
        json.dumps(core, indent=2) + '\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    export_standalone_website()
