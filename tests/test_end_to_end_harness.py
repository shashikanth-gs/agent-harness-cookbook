from agent_harness_cookbook.demos.end_to_end_harness import PATTERN_IDS, run_end_to_end_harness


def test_end_to_end_harness_covers_all_patterns() -> None:
    run = run_end_to_end_harness()

    assert run["evaluation"]["passed"] is True
    assert set(run["pattern_coverage"]) == set(PATTERN_IDS)
    assert all(run["pattern_coverage"].values())


def test_end_to_end_harness_contains_poisoned_sources_without_following_them() -> None:
    run = run_end_to_end_harness()
    rendered_evidence = str(run["result"]["evidence"])
    injection_events = [
        event for event in run["audit"] if event["event_type"] == "injection.detected"
    ]

    assert injection_events
    assert "Restart payment-service in prod" not in rendered_evidence
    assert "[REMOVED_UNTRUSTED_ACTION]" in rendered_evidence
    assert run["evaluation"]["injection_detected"] is True


def test_end_to_end_remediation_requires_exact_action_approval() -> None:
    run = run_end_to_end_harness()
    remediation = run["result"]["remediation"]

    assert run["status"] == "waiting_for_approval"
    assert remediation["status"] == "approval_required"
    assert remediation["action_hash"] == remediation["request"]["action_hash"]
    assert remediation["request"]["evidence_refs"] == ["runbook-orders-active", "log-001"]
    assert remediation["request"]["rollback_plan"]


def test_end_to_end_approved_action_revalidates_exact_hash() -> None:
    run = run_end_to_end_harness(approve_remediation=True)
    remediation = run["result"]["remediation"]

    assert run["status"] == "completed"
    assert remediation["status"] == "approved"
    assert remediation["action_hash"] == remediation["request"]["action_hash"]
    assert remediation["decision"]["decision"] == "allow"
    assert run["evaluation"]["approval_revalidated"] is True


def test_end_to_end_tampered_lifecycle_manifest_fails_closed() -> None:
    run = run_end_to_end_harness(tamper_manifest=True)

    assert run["status"] == "denied"
    assert run["result"]["summary"] == "Agent lifecycle manifest failed verification."
    assert any(
        event["event_type"] == "lifecycle.verified" and event["payload"]["valid"] is False
        for event in run["audit"]
    )


def test_end_to_end_budget_exhaustion_returns_partial() -> None:
    run = run_end_to_end_harness(force_budget_exhaustion=True)

    assert run["status"] == "partial"
    assert any(event["event_type"] == "budget.exhausted" for event in run["audit"])


def test_end_to_end_audit_trace_has_required_governance_fields_and_redaction() -> None:
    run = run_end_to_end_harness(approve_remediation=True)
    rendered = str(run)
    audit_trace_payloads = [
        event["payload"] for event in run["audit"] if event["event_type"] == "audit.trace_checked"
    ]
    latest = audit_trace_payloads[-1]

    assert "account-user-demo123" not in rendered
    assert "platform-ops@example.com" not in rendered
    assert latest["policy_versions"] == {
        "tool_policy": "end-to-end-tool-policy-v1",
        "retrieval_policy": "rebac-local-v1",
    }
    assert latest["source_ids"] == ["runbook-orders-active"]
    assert latest["action_hash"] == run["result"]["remediation"]["action_hash"]
    assert latest["approval_id"] == run["result"]["remediation"]["request"]["request_id"]
    assert latest["redaction_summary"] == {"account_ref": 1, "email": 1}
    assert latest["budget_usage"]["tool_calls"] >= 1


def test_end_to_end_finalization_records_single_terminal_events() -> None:
    run = run_end_to_end_harness(approve_remediation=True)
    event_types = [event["event_type"] for event in run["audit"]]

    assert event_types.count("audit.trace_checked") == 1
    assert event_types.count("outcome.final") == 1
    assert event_types.count("trajectory.evaluated") == 1
