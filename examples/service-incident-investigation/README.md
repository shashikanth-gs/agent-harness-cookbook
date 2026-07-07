# Service Incident Investigation

This generic local demo shows how harness patterns combine around an operational
agent. It avoids real product names and uses only mock data.

Scenario:

> Orders are not being processed after the latest release. Investigate the
> likely cause and recommend next steps.

Mock tools:

- `log_search`
- `metrics_lookup`
- `release_events`
- `restart_service`

The remediation tool is not executed. In production it requires human approval.
