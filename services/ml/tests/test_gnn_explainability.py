"""
services/ml/tests/test_gnn_explainability.py
Owner: Developer 1 (Data & ML Platform Engineer)

Tests GNNExplainer AttributionResult generation and schema compatibility with Developer 2.
"""

import uuid
from services.ml.src.explain.explainer import GNNExplainerEngine
from contracts.schemas.models import AttributionResult


def test_gnn_explainer_schema_compatibility():
    explainer = GNNExplainerEngine()
    incident_id = uuid.uuid4()
    graph_snapshot = {
        "nodes": [{"id": "host-01"}, {"id": "192.168.1.50"}],
        "edges": [("host-01", "192.168.1.50")]
    }

    attribution = explainer.explain(
        incident_id=incident_id,
        prediction_label="anomalous",
        confidence=0.96,
        graph_snapshot=graph_snapshot
    )

    assert isinstance(attribution, AttributionResult)
    assert attribution.incident_id == incident_id
    assert "host-01" in attribution.important_nodes
    assert len(attribution.important_edges) > 0
    assert "subgraph" in attribution.dict()
