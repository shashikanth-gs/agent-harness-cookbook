.PHONY: setup test api site dev build provider-smoke quickstart

setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -e ".[dev]"
	npm --prefix apps/demo-site install

quickstart: setup dev

test:
	pytest

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
