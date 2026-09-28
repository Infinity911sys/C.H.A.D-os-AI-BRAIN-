import json
import threading
from pathlib import Path
from urllib import request

from chad_os.kernel.context import AutonomyLevel
from chad_os.runtime.api import ApplicationServer
from chad_os.runtime.bootstrap import AppConfig, ChadOSApplication



def start_server(tmp_path: Path):
    config = AppConfig(
        kernel_mode='test',
        control_token='secret-token',
        alignment_threshold=0.95,
        autonomy_level=AutonomyLevel.A2,
        audit_log_path=tmp_path / 'audit.jsonl',
        ccp_license='active-license',
        host='127.0.0.1',
        port=0,
    )
    app = ChadOSApplication(config)
    app.boot()
    server = ApplicationServer((config.host, config.port), app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread



def api_request(url: str, token: str, payload=None):
    headers = {'Authorization': f'******'}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = request.Request(url, data=data, headers=headers)
    with request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))



def test_health_and_dashboard_endpoints(tmp_path):
    server, thread = start_server(tmp_path)
    base_url = f'http://127.0.0.1:{server.server_port}'
    try:
        with request.urlopen(f'{base_url}/healthz') as response:
            health = json.loads(response.read().decode('utf-8'))
        assert health['status'] == 'ok'

        telemetry = api_request(
            f'{base_url}/v1/telemetry',
            'secret-token',
            {'source': 'sensor-a', 'severity': 5, 'payload': {'incident': 'medical'}},
        )
        assert telemetry['dispatch']['priority'] == 'critical'

        dashboard = api_request(f'{base_url}/v1/dashboard', 'secret-token')
        assert dashboard['telemetry']['total_events'] == 1
        assert dashboard['last_dispatch']['route'] == 'Infinity911'
    finally:
        server.shutdown()
        thread.join(timeout=2)
