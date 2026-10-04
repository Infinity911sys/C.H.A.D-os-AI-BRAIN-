from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT / 'site'

CONTENT_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
}


def resolve_site_asset(path: str) -> tuple[Path, str] | None:
    normalized = path.split('?', 1)[0]
    if normalized in {'', '/'}:
        asset = SITE_ROOT / 'index.html'
    else:
        asset = SITE_ROOT / normalized.lstrip('/')

    try:
        asset.relative_to(SITE_ROOT)
    except ValueError:
        return None

    if not asset.exists() or not asset.is_file():
        return None
    return asset, CONTENT_TYPES.get(asset.suffix, 'application/octet-stream')
