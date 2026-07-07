# Agent Harness Cookbook

Agent Harness Cookbook is a practical reference for designing enterprise-grade
agent harnesses. It is not a framework. It is a cookbook of patterns, examples,
implementation specs, templates, tests, and prompts.

The repo helps engineers answer:

> I know how to build an agent. What should I consider around the agent to make
> it safer, governable, observable, auditable, reliable, and enterprise-ready?

## What This Includes

- Pattern articles and implementation specs.
- Self-contained reference packages for each implemented pattern.
- Pattern-local tests beside each reference implementation.
- A shared Python environment and dependency set at the repo root.
- A local demo API and lightweight website.
- Mock data only. No external services, cloud accounts, or real LLM keys needed.
- A current-source landscape note in `docs/07-current-agent-framework-landscape.md`
  to keep implementation choices grounded in recent framework and security docs.
- A source-review protocol in `docs/source-review-protocol.md`. Every pattern
  folder has a `source-review.md` that must be updated before that pattern is
  implemented or materially changed.

## v1 Patterns

All twelve patterns are implemented as grouped packages under `patterns/`:

- `01-tool-privilege-broker`
- `02-hitl-approval-gate`
- `03-decision-trace-and-audit`
- `04-cost-and-tool-budgeting`
- `05-redaction-boundary`
- `06-prompt-injection-and-goal-hijack`
- `07-rag-access-control-and-provenance`
- `08-memory-isolation`
- `09-sandboxed-execution`
- `10-agent-evaluations`
- `11-ci-cd-evaluation-gates`
- `12-agent-lifecycle-profile`

Each pattern contains docs, code, tests, and fixtures in one folder.

## Demo

The flagship demo is `service-incident-investigation`, a generic operations
scenario:

> Orders are not being processed after the latest release. Investigate the
> likely cause and recommend next steps.

The demo uses only mock tools: logs, metrics, release events, runbooks, audit,
redaction, budget tracking, and human approval for risky remediation.

## Local Setup

One command:

```bash
make quickstart
```

Or step by step:

```bash
make setup
make dev
```

Open:

- Website: `http://localhost:5173`
- API: `http://localhost:8000`

Run tests:

```bash
make test
```

## Optional Real Provider Testing With Embedded LiteLLM

Mock mode is the default and needs no API keys. To test with real model
providers, use the embedded LiteLLM Python SDK:

```bash
cp .env.example .env
# edit .env:
#   AHC_PROVIDER=litellm
#   AHC_MODEL=openai/gpt-4o-mini
#   OPENAI_API_KEY=...
make dev
```

Smoke test the configured provider:

```bash
.venv/bin/python scripts/smoke_provider.py
```

LiteLLM gives this repo one Python interface while users choose OpenAI,
Anthropic, NVIDIA NIM, Gemini, Bedrock, Ollama, or another supported provider
through `AHC_MODEL` and the relevant API key.

## Repository Shape

```text
patterns/<pattern>/
  README.md
  source-review.md
  article.md
  pattern.md
  adoption-levels.md
  implementation-spec.md
  eval-cases.md
  fixtures/
  pattern_<name>/
  tests/
```

This keeps each pattern easy to lift into another project while sharing one root
Python virtual environment and dependency set.
