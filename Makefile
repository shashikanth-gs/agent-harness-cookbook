.PHONY: setup test api site dev build provider-smoke nvidia-direct-smoke langgraph-litellm-smoke rag-litellm-embeddings-smoke quickstart

setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -e ".[dev]"
	npm --prefix apps/demo-site install

quickstart: setup dev

test:
	.venv/bin/python -m pytest -q

api:
	uvicorn apps.api.main:app --reload --port 8000

site:
	npm --prefix apps/demo-site run dev

dev:
	python scripts/dev.py

build:
	npm --prefix apps/demo-site run build

provider-smoke:
	python scripts/smoke_provider.py

nvidia-direct-smoke:
	python scripts/smoke_nvidia_direct.py

langgraph-litellm-smoke:
	python scripts/smoke_langgraph_litellm.py

rag-litellm-embeddings-smoke:
	python scripts/smoke_rag_litellm_embeddings.py
