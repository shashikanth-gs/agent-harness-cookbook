# Provider Gateway and LiteLLM

Last source review: 2026-07-09.

The cookbook remains runnable in mock mode with no API keys. For real provider
testing, it supports the embedded LiteLLM Python SDK so users can route requests
to OpenAI, Anthropic, NVIDIA NIM, Gemini, Azure, Bedrock, Ollama, or another
LiteLLM provider without changing the harness examples.

## Current Source Notes

- LiteLLM can be used as a Python SDK or as a proxy server / AI gateway. This
  repo uses the Python SDK path because it is simpler for a one-process local
  cookbook demo.
- LiteLLM SDK exposes `completion()` as a unified provider interface.
- LiteLLM supports NVIDIA NIM with the `nvidia_nim/` provider route and
  `https://integrate.api.nvidia.com/v1/` for chat and embeddings.

## Design Consequences

- Mock mode remains the default because this is a cookbook and should work
  without paid services.
- Real provider mode goes through the same provider abstraction used by the demo
  API.
- Provider selection is environment-driven:
- `AHC_PROVIDER=mock`
- `AHC_PROVIDER=litellm`
- The cookbook should not hard-code a single provider or model.
- Real-provider tests are smoke tests, not required CI tests, because they
  depend on external credentials and provider availability.

## Local Flow

1. Copy `.env.example` to `.env`.
2. Add one or more provider API keys.
3. Set `AHC_PROVIDER=litellm`.
4. Set `AHC_MODEL` to a LiteLLM model string such as `openai/gpt-4o-mini`,
   `anthropic/claude-3-5-haiku-latest`, or
   `nvidia_nim/mistralai/mistral-medium-3.5-128b`.
5. Start the cookbook API and site.
6. Run the provider smoke script or use the demo UI.

## Demo Model Profile

The default NVIDIA demonstration profile is:

| Role | Model | Status |
| --- | --- | --- |
| Chat / agent workflow | `nvidia_nim/mistralai/mistral-small-4-119b-2603` | Verified with LiteLLM and LangGraph |
| Direct NVIDIA chat | `mistralai/mistral-small-4-119b-2603` | Verified with direct requests |
| Embeddings / RAG | `nvidia_nim/nvidia/nv-embedqa-e5-v5` | Verified with LiteLLM embeddings |
| Rerank | `nvidia/llama-nemotron-rerank-1b-v2` | Profiled but not enabled by default |
| Judge / eval | `nvidia_nim/mistralai/mistral-small-4-119b-2603` | Uses chat model initially |

Rerank is represented as a provider slot and deterministic local reranker. The
NVIDIA rerank model is listed in the profile, but the LiteLLM rerank route was
not verified against the current NVIDIA endpoint during this pass, so
`AHC_RERANK_PROVIDER=mock` remains the default.

## NVIDIA NIM Demonstration Example

```bash
AHC_PROVIDER=litellm
AHC_MODEL=nvidia_nim/mistralai/mistral-medium-3.5-128b
NVIDIA_NIM_API_KEY=...
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
```

This uses LiteLLM's `nvidia_nim/` provider route and NVIDIA's
OpenAI-compatible chat completions endpoint.

This NVIDIA configuration is included for demonstration and smoke-testing only.
For your own use cases, choose the provider and model that fit your accuracy,
latency, cost, data residency, security, and compliance requirements. The
harness examples should remain provider-neutral; LiteLLM is the adapter that
lets you route to OpenAI, Anthropic, NVIDIA NIM, Gemini, Azure, Bedrock, Ollama,
or another supported provider.

## Direct NVIDIA Python Requests Example

For teams that want to bypass LiteLLM and call NVIDIA's OpenAI-compatible API
directly, the repo includes `NvidiaDirectChatModel`.

```bash
AHC_PROVIDER=nvidia_direct
AHC_MODEL=mistralai/mistral-small-4-119b-2603
NVIDIA_API_KEY=...
NVIDIA_NIM_INVOKE_URL=https://integrate.api.nvidia.com/v1/chat/completions
.venv/bin/python scripts/smoke_nvidia_direct.py
```

The direct path is useful for validating provider payload details such as
`reasoning_effort`, `temperature`, `top_p`, and provider-specific model names.
The LiteLLM path is better when you want one provider abstraction across many
model vendors.

## LangGraph With LiteLLM

The service-incident demo also has a LangGraph implementation:

```bash
AHC_PROVIDER=litellm
AHC_MODEL=nvidia_nim/mistralai/mistral-small-4-119b-2603
NVIDIA_NIM_API_KEY=...
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
.venv/bin/python scripts/smoke_langgraph_litellm.py
```

This runs a real LangGraph workflow with separate graph nodes for request
initialization, model classification, evidence gathering, synthesis, and
approval gating. The graph still uses the same harness controls: tool broker,
audit, trace, budget, redaction, and HITL approval.

## Verified Smoke Test

Verified on 2026-07-09:

- Provider: LiteLLM Python SDK
- Route: `nvidia_nim/`
- Model: `mistralai/mistral-small-4-119b-2603`
- Endpoint base: `https://integrate.api.nvidia.com/v1`
- Cookbook path tested: `run_investigation(..., request_remediation=True)`
- LangGraph path tested: `run_langgraph_investigation(..., request_remediation=True)`
- Expected harness behavior: model classification uses LiteLLM/NVIDIA, mock tool
  evidence is gathered, and production remediation still returns
  `approval_required`.

Also verified on 2026-07-09:

- Provider: direct NVIDIA Python requests
- Model: `mistralai/mistral-small-4-119b-2603`
- Endpoint: `https://integrate.api.nvidia.com/v1/chat/completions`
- Script: `scripts/smoke_nvidia_direct.py`
- Expected behavior: visible assistant content is extracted without storing
  provider reasoning fields.

Also verified on 2026-07-09:

- Provider: LiteLLM embeddings
- Model: `nvidia_nim/nvidia/nv-embedqa-e5-v5`
- Script: `scripts/smoke_rag_litellm_embeddings.py`
- Expected behavior: authorized active document is retrieved with provenance,
  1024-dimensional embeddings are returned, and citation validation passes.

Do not commit real provider keys. Use `.env` or shell environment variables for
temporary testing.
