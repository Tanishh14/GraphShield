"""
services/agents/tests/test_langgraph_pipeline.py
Owner: Developer 2 (Agent & Intelligence API Engineer)

LangGraph Pipeline & State Machine Transition Tests.
"""

import pytest
import uuid
from contracts.schemas.models import GNNPrediction, AttributionResult
from services.agents.src.pipeline import LangGraphPipeline
from services.agents.tests.fixtures.mock_ml_producer import generate_mock_ml_prediction_and_attribution


def test_pipeline_execution_successful_flow():
    pred_payload, attr_payload = generate_mock_ml_prediction_and_attribution("host-test-01")
    
    prediction = GNNPrediction(**pred_payload)
    attribution = AttributionResult(**attr_payload)

    initial_state = {
        "incident_id": str(attribution.incident_id),
        "prediction": prediction,
        "attribution": attribution,
        "investigation_result": None,
        "threat_intel_result": None,
        "report": None,
        "proposed_remediation": None,
        "retries": 0,
        "status": "running"
    }

    pipeline = LangGraphPipeline()
    final_state = pipeline.run(initial_state)

    assert final_state["status"] == "complete"
    assert final_state["investigation_result"] is not None
    assert final_state["threat_intel_result"] is not None
    assert final_state["report"] is not None
    assert final_state["proposed_remediation"] is not None
    assert final_state["proposed_remediation"].target == "host-test-01"
