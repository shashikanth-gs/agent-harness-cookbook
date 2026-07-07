from pattern_redaction_boundary import redact_demo_payload


def test_redacts_email_and_account_reference() -> None:
    redacted = str(redact_demo_payload())
    assert "alex@example.com" not in redacted
    assert "account-user-abc123" not in redacted
    assert "[REDACTED:email]" in redacted
    assert "[REDACTED:account_ref]" in redacted


def test_redacts_token_key_and_card() -> None:
    redacted = str(redact_demo_payload())
    assert "Bearer abcdefghijklmnopqrstuvwxyz123456" not in redacted
    assert "sk_abcdefghijklmnop123456" not in redacted
    assert "4111 1111 1111 1111" not in redacted
    assert "[REDACTED:bearer_token]" in redacted
    assert "[REDACTED:api_key]" in redacted
    assert "[REDACTED:credit_card]" in redacted
