from relaytrace_strands_adapter import RelayTraceDecisionClient, relaytrace_supervised


def test_symbols_exist() -> None:
    assert RelayTraceDecisionClient is not None
    assert relaytrace_supervised is not None
