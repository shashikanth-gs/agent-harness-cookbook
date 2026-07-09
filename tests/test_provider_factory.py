from agent_harness_cookbook.providers.factory import get_model_provider
from agent_harness_cookbook.providers.model_profiles import NVIDIA_DEMO_PROFILE, get_model_profile
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


def test_provider_factory_supports_nvidia_direct(monkeypatch) -> None:
    monkeypatch.setenv("NVIDIA_API_KEY", "test-key")
    provider = get_model_provider("nvidia_direct")
    assert provider.__class__.__name__ == "NvidiaDirectChatModel"


def test_nvidia_demo_profile_has_chat_and_embedding_models() -> None:
    assert NVIDIA_DEMO_PROFILE.chat_model.startswith("nvidia_nim/")
    assert "embed" in NVIDIA_DEMO_PROFILE.embedding_model


def test_model_profile_can_be_overridden(monkeypatch) -> None:
    monkeypatch.setenv("AHC_CHAT_MODEL", "nvidia_nim/example/chat")
    assert get_model_profile().chat_model == "nvidia_nim/example/chat"
