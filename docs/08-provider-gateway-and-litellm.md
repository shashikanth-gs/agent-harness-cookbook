# Provider Gateway and LiteLLM

Last source review: 2026-07-04.

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
   `nvidia_nim/meta/llama-3.1-70b-instruct`.
5. Start the cookbook API and site.
6. Run the provider smoke script or use the demo UI.
