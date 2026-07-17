.PHONY: setup test api site dev build provider-smoke nvidia-direct-smoke langgraph-litellm-smoke rag-litellm-embeddings-smoke quickstart

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e ".[dev]"
	npm --prefix apps/demo-site install

quickstart: setup dev

test:
	.venv/bin/python -m pytest -q

api:
	.venv/bin/python -m uvicorn apps.api.main:app --reload --port 8000

site:
	npm --prefix apps/demo-site run dev

dev:
	.venv/bin/python scripts/dev.py

build:
	npm --prefix apps/demo-site run build

provider-smoke:
	.venv/bin/python scripts/smoke_provider.py

nvidia-direct-smoke:
	.venv/bin/python scripts/smoke_nvidia_direct.py

langgraph-litellm-smoke:
	.venv/bin/python scripts/smoke_langgraph_litellm.py

rag-litellm-embeddings-smoke:
	.venv/bin/python scripts/smoke_rag_litellm_embeddings.py
