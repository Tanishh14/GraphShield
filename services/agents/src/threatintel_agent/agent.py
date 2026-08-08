import logging
from uuid import UUID
from typing import Dict, Any
from contracts.schemas.models import ThreatIntelResult, InvestigationResult
from services.agents.src.graph_state import AgentState
from services.agents.src.threatintel_agent.tools import PgVectorRetrievalTool

logger = logging.getLogger("threatintel_agent")


class ThreatIntelAgent:
    """
    Threat-Intel Agent (Agent 2 in LangGraph Pipeline).
    Uses pgvector RAG tool to retrieve local MITRE ATT&CK & CVE evidence without web access.
    Strictly separates retrieved_evidence (with citations) from interpretation synthesis.
    """

    def __init__(self, retrieval_tool: PgVectorRetrievalTool = None):
        self.retrieval_tool = retrieval_tool or PgVectorRetrievalTool()

    def run(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"[ThreatIntelAgent] Starting threat intel lookup for incident: {state['incident_id']}")
        
        inv_res: InvestigationResult = state.get("investigation_result")
        query_context = "GNN anomalous behavior lateral movement valid accounts"
        if inv_res:
            query_context += f" affected entities: {', '.join(inv_res.affected_entities)}"

        # Perform local RAG retrieval
        evidence_chunks = self.retrieval_tool.similarity_search(query_text=query_context, top_k=5)

        matched_techniques = []
        matched_cves = []
        for chunk in evidence_chunks:
            if "technique_id" in chunk:
                matched_techniques.append(chunk["technique_id"])
            if "cve_id" in chunk:
                matched_cves.append(chunk["cve_id"])

        synthesis_interpretation = (
            f"The observed behavioral pattern aligns with MITRE ATT&CK techniques ({', '.join(matched_techniques)}) "
            f"and vulnerability disclosures ({', '.join(matched_cves)}). "
            "Credential misuse combined with local privilege escalation indicates an active targeted attack campaign."
        )

        threat_intel_res = ThreatIntelResult(
            incident_id=UUID(state["incident_id"]),
            retrieved_evidence=evidence_chunks,
            interpretation=synthesis_interpretation,
            matched_techniques=matched_techniques,
            matched_cves=matched_cves
        )

        logger.info(f"[ThreatIntelAgent] Threat intel matching complete for incident: {state['incident_id']}")
        return {"threat_intel_result": threat_intel_res}
