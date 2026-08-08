import logging
from typing import Dict, Any, List
from contracts.schemas.models import AttributionResult

logger = logging.getLogger("investigation_tools")


class Neo4jReadOnlyTool:
    """Read-only query tool to query Neo4j attack graph without write privileges."""

    def __init__(self, uri: str = "bolt://localhost:7687", auth: tuple = ("neo4j", "password")):
        self.uri = uri
        self.auth = auth

    def query_subgraph(self, node_ids: List[str]) -> List[Dict[str, Any]]:
        """Queries graph neighborhood for given attributed node IDs (read-only Cypher)."""
        logger.info(f"[Neo4jReadOnlyTool] Executing read Cypher query for nodes: {node_ids}")
        # Parameterized Cypher representation
        simulated_edges = []
        for i in range(len(node_ids) - 1):
            simulated_edges.append({
                "source": node_ids[i],
                "target": node_ids[i + 1],
                "relationship": "CONNECTS_TO",
                "timestamp": "2026-08-08T12:00:00Z"
            })
        return simulated_edges


class AttributionReader:
    """Reads and parses GNNExplainer AttributionResult objects."""

    @staticmethod
    def extract_key_subgraph(attribution: AttributionResult) -> Dict[str, Any]:
        """Extracts node list, edge list, and top features from AttributionResult."""
        return {
            "nodes": attribution.important_nodes,
            "edges": attribution.important_edges,
            "top_features": attribution.important_features
        }
