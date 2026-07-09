from agent_harness_cookbook.providers.nvidia_direct import _visible_content


def test_visible_content_strips_provider_think_marker() -> None:
    assert _visible_content({"content": "[THINK]nvidia direct ok"}) == "nvidia direct ok"


def test_visible_content_does_not_return_reasoning_content() -> None:
    assert (
        _visible_content({"content": None, "reasoning_content": "hidden reasoning"})
        == "Provider returned no visible message content."
    )
