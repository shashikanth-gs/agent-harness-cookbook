from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_harness_cookbook.demos.pattern_catalog import run_pattern_catalog
from agent_harness_cookbook.demos.service_incident_investigation import run_investigation


class InvestigationRequest(BaseModel):
    request: str = "Orders are not being processed after the latest release. Investigate the likely cause and recommend next steps."
    request_remediation: bool = False


app = FastAPI(title="Agent Harness Cookbook API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/demos/service-incident-investigation")
def service_incident_investigation(request: InvestigationRequest) -> dict[str, object]:
    return run_investigation(request.request, request.request_remediation)


@app.get("/patterns/run-all")
def run_all_patterns() -> dict[str, object]:
    return run_pattern_catalog()
