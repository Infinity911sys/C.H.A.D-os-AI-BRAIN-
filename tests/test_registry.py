from chad_os.services.registry import SystemRegistry



def test_registry_contains_all_125_systems():
    registry = SystemRegistry.load()
    assert registry.metadata['system_count'] == 125
    assert len(registry.systems) == 125



def test_core_contracts_match_core_systems():
    registry = SystemRegistry.load()
    contract_ids = {item['id'] for item in registry.core_contracts['systems']}
    core_ids = {item['id'] for item in registry.core_systems()}
    assert contract_ids == core_ids
