from agent_harness_cookbook.providers.factory import get_model_provider
from agent_harness_cookbook.providers.mock_model import MockModel


def test_provider_factory_defaults_to_mock(monkeypatch) -> None:
    monkeypatch.delenv("AHC_PROVIDER", raising=False)
    assert isinstance(get_model_provider(), MockModel)


def test_provider_factory_rejects_unknown_provider() -> None:
    try:
        get_model_provider("unknown")
    except ValueError as exc:
        assert "unknown provider" in str(exc)
    else:
        raise AssertionError("expected ValueError")
