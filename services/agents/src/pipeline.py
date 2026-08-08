import logging
from typing import Dict, Any, Literal
from services.agents.src.graph_state import AgentState
from services.agents.src.investigation_agent.agent import InvestigationAgent
from services.agents.src.threatintel_agent.agent import ThreatIntelAgent
from services.agents.src.actionreport_agent.agent import ActionReportAgent

logger = logging.getLogger("langgraph_pipeline")


class LangGraphPipeline:
    """
    State-Machine Orchestrator for SentinelGraph Agent Plane.
    Executes Agent 1 (Investigation) -> Agent 2 (ThreatIntel) -> Agent 3 (ActionReport) sequentially.
    Handles retry loops (max 2 retries) and terminal failure routing to NEEDS_HUMAN_TRIAGE.
    """

    MAX_RETRIES = 2

    def __init__(self):
        self.investigation_agent = InvestigationAgent()
        self.threat_intel_agent = ThreatIntelAgent()
        self.action_report_agent = ActionReportAgent()

    def run(self, initial_state: AgentState) -> AgentState:
        state = dict(initial_state)
        state["status"] = "running"

        logger.info(f"[LangGraphPipeline] Starting pipeline for incident {state['incident_id']} (retries={state['retries']})")

        try:
            # Step 1: Investigation Agent
            inv_output = self.investigation_agent.run(state)
            state.update(inv_output)

            # Step 2: Threat-Intel Agent
            intel_output = self.threat_intel_agent.run(state)
            state.update(intel_output)

            # Step 3: Action & Report Agent
            report_output = self.action_report_agent.run(state)
            state.update(report_output)

            # Check grounding validator result
            if state["report"] and not state["report"].grounded:
                if state["retries"] < self.MAX_RETRIES:
                    logger.warning(f"[LangGraphPipeline] Grounding failed. Retrying pipeline (retry {state['retries'] + 1}/{self.MAX_RETRIES})")
                    state["retries"] += 1
                    state["status"] = "needs_retry"
                    return self.run(state)
                else:
                    logger.error(f"[LangGraphPipeline] Max retries exhausted for incident {state['incident_id']}. Routing to NEEDS_HUMAN_TRIAGE.")
                    state["status"] = "failed"
                    return state

            state["status"] = "complete"
            logger.info(f"[LangGraphPipeline] Pipeline execution successfully completed for incident {state['incident_id']}")
            return state

        except Exception as e:
            logger.error(f"[LangGraphPipeline] Exception during pipeline execution: {str(e)}")
            if state["retries"] < self.MAX_RETRIES:
                state["retries"] += 1
                state["status"] = "needs_retry"
                return self.run(state)
            else:
                state["status"] = "failed"
                return state
