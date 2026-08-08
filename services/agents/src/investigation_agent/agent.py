import logging
from uuid import UUID
from typing import Dict, Any
from contracts.schemas.models import InvestigationResult, AttributionResult
from services.agents.src.graph_state import AgentState
from services.agents.src.investigation_agent.tools import Neo4jReadOnlyTool, AttributionReader

logger = logging.getLogger("investigation_agent")


class InvestigationAgent:
    """
    Investigation Agent (Agent 1 in LangGraph Pipeline).
    Correlates predictions, reconstructs attack path from attributed subgraph using read-only Neo4j tool,
    and produces an InvestigationResult.
    STRICTLY NO REMEDIATION OR SIDE-EFFECT TOOLS.
    """

    def __init__(self, neo4j_tool: Neo4jReadOnlyTool = None):
        self.neo4j_tool = neo4j_tool or Neo4jReadOnlyTool()

    def run(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"[InvestigationAgent] Starting investigation for incident: {state['incident_id']}")
        
        attribution: AttributionResult = state["attribution"]
        if not attribution:
            raise ValueError("AttributionResult missing in state for InvestigationAgent.")

        # Read key subgraph elements from attribution
        subgraph_summary = AttributionReader.extract_key_subgraph(attribution)
        important_nodes = subgraph_summary["nodes"]
        
        # Query Neo4j read-only tool to trace attack path relationships
        graph_edges = self.neo4j_tool.query_subgraph(important_nodes)

        attack_path = []
        timeline = []
        for idx, edge in enumerate(graph_edges):
            attack_path.append({
                "step": idx + 1,
                "source": edge["source"],
                "target": edge["target"],
                "action": edge["relationship"]
            })
            timeline.append({
                "timestamp": edge["timestamp"],
                "event": f"Entity {edge['source']} executed {edge['relationship']} to {edge['target']}"
            })

        investigation_res = InvestigationResult(
            incident_id=UUID(state["incident_id"]),
            summary=f"GNN anomaly detected on target node {state['prediction'].target_node_id if state['prediction'] else 'unknown'}. Attack path reconstructed across {len(important_nodes)} entities.",
            affected_entities=important_nodes,
            attack_path=attack_path,
            timeline=timeline,
            correlation_notes="Correlated flows indicate lateral movement and suspicious port connectivity."
        )

        logger.info(f"[InvestigationAgent] Completed attack path reconstruction for incident: {state['incident_id']}")
        return {"investigation_result": investigation_res}
