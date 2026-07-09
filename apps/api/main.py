from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_harness_cookbook.demos.pattern_catalog import run_pattern_catalog
from agent_harness_cookbook.demos.rag_governance import run_rag_governance_demo
from agent_harness_cookbook.demos.service_incident_investigation import run_investigation
from agent_harness_cookbook.demos.service_incident_langgraph import run_langgraph_investigation


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


@app.post("/demos/service-incident-investigation/langgraph")
def service_incident_investigation_langgraph(request: InvestigationRequest) -> dict[str, object]:
    return run_langgraph_investigation(request.request, request.request_remediation)


@app.get("/patterns/run-all")
def run_all_patterns() -> dict[str, object]:
    return run_pattern_catalog()


@app.get("/demos/rag-governance")
def rag_governance(query: str = "Which API retrieves order details and what field is required?") -> dict[str, object]:
    return run_rag_governance_demo(query)
