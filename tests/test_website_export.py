import json

from chad_os.runtime.export_website import export_standalone_website


def test_standalone_website_export_creates_data_files(tmp_path):
    export_standalone_website(tmp_path)

    summary = json.loads((tmp_path / 'data' / 'summary.json').read_text(encoding='utf-8'))
    catalog = json.loads((tmp_path / 'data' / 'catalog.json').read_text(encoding='utf-8'))
    core = json.loads((tmp_path / 'data' / 'core.json').read_text(encoding='utf-8'))

    assert summary['summary']['system_count'] == 125
    assert catalog['count'] == 125
    assert core['systems']
