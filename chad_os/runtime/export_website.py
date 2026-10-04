from __future__ import annotations

from pathlib import Path
import json

from chad_os.services.algotraj import AlgoTrajService
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
    algotraj = AlgoTrajService()
    algotraj_product = {
        'summary': algotraj.summary(),
        'play_store': algotraj.play_store_readiness(),
        'today_prompts': [
            {
                'title': 'Trajectory correction map',
                'body': 'Map a behavioral-trajectory correction flow for a route that has unstable deviations and define the stabilization loop.',
            },
            {
                'title': 'Vector anomaly review',
                'body': 'Analyze a spatial vector stream, identify deviation clusters, and rank which pathway corrections should happen first.',
            },
            {
                'title': 'Stabilized route architecture',
                'body': 'Design an enterprise-grade Algo-Traj architecture for corrected pathways, optimization loops, and audit visibility.',
            },
            {
                'title': 'Mobile operator view',
                'body': 'Define the Play-Store-ready mobile experience for Algo-Traj operators who need trajectory alerts, correction states, and vector maps.',
            },
        ],
    }

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
    (data_dir / 'algotraj.json').write_text(
        json.dumps(algotraj_product, indent=2) + '\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    export_standalone_website()
