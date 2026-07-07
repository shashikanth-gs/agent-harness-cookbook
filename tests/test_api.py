from fastapi.testclient import TestClient

from apps.api.main import app


def test_run_all_patterns_endpoint() -> None:
    response = TestClient(app).get("/patterns/run-all")
    assert response.status_code == 200
    payload = response.json()
    assert len([key for key in payload if key[:2].isdigit()]) == 12


def test_service_incident_endpoint() -> None:
    response = TestClient(app).post(
        "/demos/service-incident-investigation",
        json={"request": "Orders are delayed after the latest release.", "request_remediation": True},
    )
    assert response.status_code == 200
    assert response.json()["result"]["remediation"]["status"] == "approval_required"
