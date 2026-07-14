# Reference Architecture

This reference architecture keeps the repo local-first while showing enterprise
harness controls.

```text
user request
  -> input classifier
  -> task intent extractor
  -> source trust classifier
  -> retrieval guard
  -> context builder
  -> model/agent loop
  -> tool privilege broker
  -> approval gate when required
  -> sandbox or tool runtime
  -> redaction boundary
  -> audit sink
  -> eval sink
```

## Local-First Components

Use:

- mock tools,
- local JSON fixtures,
- local policies,
- local traces,
- local eval runner,
- safe simulated execution.

Do not require:

- real Splunk,
- real Prometheus,
- real Azure,
- real OpenAI key,
- real database,
- Kubernetes,
- cloud account.

## Enterprise Adapters

Optional adapters can later map the same boundaries to:

- managed identities,
- scoped credentials,
- private endpoints,
- API gateways,
- SIEM export,
- WORM retention,
- OpenTelemetry,
- cloud log analytics,
- rate limits,
- kill switches.

The cookbook should keep the boundary clear even when the backing service
changes.
