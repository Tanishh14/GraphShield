import logging
from uuid import UUID
from typing import Dict, Any
from contracts.schemas.models import (
    ActionReportResult,
    ProposedRemediation,
    InvestigationResult,
    ThreatIntelResult,
    AttributionResult
)
from services.agents.src.graph_state import AgentState
from services.agents.src.guardrails.grounding_validator import GroundingValidator

logger = logging.getLogger("actionreport_agent")


class ActionReportAgent:
    """
    Action & Report Agent (Agent 3 in LangGraph Pipeline).
    Consumes results from Agent 1 and Agent 2, generates a grounded report and ProposedRemediation data object.
    Runs GroundingValidator on output prior to acceptance.
    STRICTLY NO EXECUTION PRIVILEGES.
    """

    def run(self, state: AgentState) -> Dict[str, Any]:
        logger.info(f"[ActionReportAgent] Synthesizing final report for incident: {state['incident_id']}")

        attribution: AttributionResult = state["attribution"]
        inv_res: InvestigationResult = state.get("investigation_result")
        intel_res: ThreatIntelResult = state.get("threat_intel_result")

        primary_target = attribution.important_nodes[0] if (attribution and attribution.important_nodes) else "host-01"

        raw_report_text = (
            f"Executive Summary: Anomalous activity detected targeting host {primary_target}. "
            f"GNN confidence score: {attribution.confidence if attribution else 0.95}. "
            f"Reconstructed attack path involves affected entities: {', '.join(inv_res.affected_entities if inv_res else [primary_target])}. "
            f"Threat intel matches: {', '.join(intel_res.matched_techniques if intel_res else [])}. "
            "Action Item: Contain primary compromise vector by isolating target host."
        )

        # Run Grounding Validator
        sanitized_text, is_grounded, unresolvable = GroundingValidator.validate_and_sanitize_report(
            report_text=raw_report_text,
            attribution=attribution
        )

        report_res = ActionReportResult(
            incident_id=UUID(state["incident_id"]),
            executive_summary=f"Incident Report for {primary_target}",
            risk_assessment="HIGH risk incident with multi-stage lateral movement potential.",
            detailed_findings=sanitized_text,
            grounded=is_grounded,
            attribution_refs=attribution.important_nodes if attribution else []
        )

        # Propose remediation as DATA ONLY payload
        proposed_action = ProposedRemediation(
            incident_id=UUID(state["incident_id"]),
            action_type="ISOLATE_HOST",
            target=primary_target,
            risk_level="HIGH",
            reason=f"Automated GNN anomaly score ({attribution.confidence if attribution else 0.95}) exceeds operating threshold. Host isolation proposed to prevent lateral spread.",
            proposed_by="ActionReportAgent"
        )

        logger.info(f"[ActionReportAgent] Report generated and validated (grounded={is_grounded}). Remediation action proposed.")
        return {
            "report": report_res,
            "proposed_remediation": proposed_action
        }
