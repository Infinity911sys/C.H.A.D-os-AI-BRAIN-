from chad_os.services.algotraj import AlgoTrajService


def test_algotraj_analysis_includes_device_monitoring_scope():
    service = AlgoTrajService()
    result = service.analyze(
        {
            'route_name': 'phoenix-corridor',
            'severity': 4,
            'route_pressure': 0.72,
            'vector_confidence': 0.83,
            'deviation_count': 3,
        }
    )

    assert result['monitoring_scope']['mode'] == 'authorized-device-ingress'
    assert 'notifications' in result['observed_inputs']
    assert result['correction_priority'] in {'priority', 'critical'}
