"""
services/agents/tests/fixtures/mock_ml_producer.py
Owner: Developer 2 (Agent & Intelligence API Engineer)

Produces schema-valid mock GNNPrediction and AttributionResult events for independent Dev 2 testing.
"""

import uuid
from datetime import datetime
from typing import Tuple, Dict, Any


def generate_mock_ml_prediction_and_attribution(
    target_node: str = "host-01",
    confidence: float = 0.96
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    incident_id = str(uuid.uuid4())
    prediction_id = str(uuid.uuid4())

    prediction_payload = {
        "incident_candidate_id": incident_id,
        "model_version": "graphsage-v1.0.0",
        "prediction": "anomalous",
        "confidence": confidence,
        "anomaly_score": 0.96,
        "target_node_id": target_node,
        "timestamp": datetime.utcnow().isoformat()
    }

    attribution_payload = {
        "incident_id": incident_id,
        "model_version": "graphsage-v1.0.0",
        "prediction": "anomalous",
        "confidence": confidence,
        "important_nodes": [target_node, "192.168.1.50", "ws-finance-02"],
        "important_edges": [
            (target_node, "192.168.1.50"),
            ("192.168.1.50", "ws-finance-02")
        ],
        "important_features": {
            "flow_bytes_per_sec": 0.89,
            "port_count_window": 0.94,
            "failed_login_count": 0.98
        },
        "subgraph": {
            "nodes": [
                {"id": target_node, "label": "Host", "ip": "10.0.0.1"},
                {"id": "192.168.1.50", "label": "IP", "ip": "192.168.1.50"},
                {"id": "ws-finance-02", "label": "Host", "ip": "10.0.0.5"}
            ],
            "edges": [
                {"source": target_node, "target": "192.168.1.50", "relation": "CONNECTS_TO"},
                {"source": "192.168.1.50", "target": "ws-finance-02", "relation": "AUTHENTICATED_TO"}
            ]
        }
    }

    return prediction_payload, attribution_payload
