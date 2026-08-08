import pytest
from services.api.src.routes.health import health_check, readiness_check
from services.api.src.routes.incidents import list_incidents, get_incident_detail
from services.api.src.routes.graph import get_cytoscape_graph


def test_health_check():
    response = health_check()
    assert response["status"] == "ok"


def test_readiness_check():
    response = readiness_check()
    assert response["status"] == "ready"


def test_list_incidents():
    incidents = list_incidents()
    assert isinstance(incidents, list)
    assert len(incidents) > 0


def test_get_incident_detail():
    incident_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    data = get_incident_detail(incident_id)
    assert "incident" in data
    assert "agent_reports" in data


def test_get_cytoscape_graph():
    incident_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    data = get_cytoscape_graph(incident_id)
    assert "elements" in data
    assert "nodes" in data["elements"]
    assert "edges" in data["elements"]
