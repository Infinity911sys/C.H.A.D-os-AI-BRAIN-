from pathlib import Path

from chad_os.runtime.bootstrap import AppConfig, ChadOSApplication
from chad_os.kernel.context import AutonomyLevel



def build_app(tmp_path: Path) -> ChadOSApplication:
    config = AppConfig(
        kernel_mode='test',
        control_token='secret-token',
        alignment_threshold=0.95,
        autonomy_level=AutonomyLevel.A2,
        audit_log_path=tmp_path / 'audit.jsonl',
        ccp_license='active-license',
    )
    app = ChadOSApplication(config)
    app.boot()
    return app



def test_boot_and_telemetry_dispatch(tmp_path):
    app = build_app(tmp_path)
    result = app.ingest_telemetry(
        {
            'source': 'sentinel-link',
            'severity': 4,
            'location': 'Phoenix',
            'payload': {'incident': 'fire'},
        }
    )
    assert result['dispatch']['priority'] == 'urgent'
    assert result['dispatch']['recommended_unit'] == 'Autonomous Dispatch Coordinator'
    assert app.audit.tail(2)



def test_reasoning_prompt_records_audit(tmp_path):
    app = build_app(tmp_path)
    result = app.process_prompt('Hello world')
    assert result['valid'] is True
    assert 'Stub answer to: Hello world' == result['answer']
