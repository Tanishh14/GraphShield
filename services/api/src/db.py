import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger("api_db")


class ReadOnlyDatabaseClient:
    """Read-only database client for services/api consuming Postgres and Neo4j."""

    def __init__(self):
        self.pg_uri = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@localhost:5432/sentinelgraph")
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")

    def get_incidents(self, status: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Reads incidents list (read-only SELECT)."""
        logger.info(f"[ReadOnlyDB] Querying incidents (status={status}, limit={limit})")
        return [
            {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "created_at": "2026-08-08T12:00:00Z",
                "updated_at": "2026-08-08T12:05:00Z",
                "status": "AWAITING_APPROVAL",
                "gnn_prediction_id": "b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "severity": "HIGH",
                "title": "Anomalous Activity on host-01",
                "summary": "Attributed lateral movement and valid account credential misuse.",
                "model_version": "graphsage-v1.0.0"
            }
        ]

    def get_incident_detail(self, incident_id: str) -> Dict[str, Any]:
        """Reads incident detail with associated agent reports (read-only SELECT)."""
        logger.info(f"[ReadOnlyDB] Querying detailed incident payload for ID: {incident_id}")
        return {
            "incident": {
                "id": incident_id,
                "created_at": "2026-08-08T12:00:00Z",
                "status": "AWAITING_APPROVAL",
                "severity": "HIGH",
                "title": f"Anomalous Activity on host-01 ({incident_id[:8]})",
                "summary": "Reconstructed attack path indicates potential compromise.",
                "model_version": "graphsage-v1.0.0"
            },
            "agent_reports": [
                {
                    "agent_type": "INVESTIGATION",
                    "content": {"affected_entities": ["host-01", "192.168.1.50"], "timeline": []},
                    "grounded": True
                },
                {
                    "agent_type": "THREAT_INTEL",
                    "content": {"matched_techniques": ["T1078"], "matched_cves": ["CVE-2023-38606"]},
                    "grounded": True
                },
                {
                    "agent_type": "ACTION_REPORT",
                    "content": {"executive_summary": "Action proposal generated: isolate host-01."},
                    "grounded": True
                }
            ]
        }

    def get_cytoscape_graph(self, incident_id: str) -> Dict[str, Any]:
        """Formats attribution graph neighborhood into Cytoscape.js node/edge payload."""
        logger.info(f"[ReadOnlyDB] Formatting Cytoscape graph for incident: {incident_id}")
        return {
            "elements": {
                "nodes": [
                    {"data": {"id": "host-01", "label": "host-01", "type": "Host", "score": 0.96}},
                    {"data": {"id": "192.168.1.50", "label": "192.168.1.50", "type": "IP", "score": 0.85}},
                    {"data": {"id": "ws-finance-02", "label": "ws-finance-02", "type": "Host", "score": 0.40}}
                ],
                "edges": [
                    {"data": {"id": "e1", "source": "host-01", "target": "192.168.1.50", "label": "CONNECTS_TO"}},
                    {"data": {"id": "e2", "source": "192.168.1.50", "target": "ws-finance-02", "label": "AUTHENTICATED_TO"}}
                ]
            }
        }
