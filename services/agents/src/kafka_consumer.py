import json
import logging
import uuid
from typing import Dict, Any
from contracts.schemas.models import GNNPrediction, AttributionResult, Incident
from services.agents.src.graph_state import AgentState
from services.agents.src.pipeline import LangGraphPipeline

logger = logging.getLogger("agent_kafka_handler")


class AgentKafkaHandler:
    """
    Kafka Event Handler for Developer 2.
    Consumes ml.predictions and ml.attributions, executes LangGraph agent pipeline,
    persists incidents and reports to Postgres, and emits incidents.created and remediation.proposals.
    """

    def __init__(self):
        self.pipeline = LangGraphPipeline()
        self.processed_events = set()  # In-memory deduplication set (Postgres handles persistent dedup)

    def process_incoming_ml_event(self, prediction_payload: Dict[str, Any], attribution_payload: Dict[str, Any]) -> Dict[str, Any]:
        event_id = prediction_payload.get("event_id", str(uuid.uuid4()))
        if event_id in self.processed_events:
            logger.info(f"Duplicate event_id {event_id} received. Skipping processing (Idempotent Handler).")
            return {"status": "skipped_duplicate"}

        self.processed_events.add(event_id)

        # Validate incoming payloads against contracts
        prediction = GNNPrediction(**prediction_payload)
        attribution = AttributionResult(**attribution_payload)

        incident_id = str(attribution.incident_id)

        # Assemble initial state for LangGraph pipeline
        initial_state: AgentState = {
            "incident_id": incident_id,
            "prediction": prediction,
            "attribution": attribution,
            "investigation_result": None,
            "threat_intel_result": None,
            "report": None,
            "proposed_remediation": None,
            "retries": 0,
            "status": "running"
        }

        # Run pipeline
        final_state = self.pipeline.run(initial_state)

        # Format output Kafka payloads
        incident_status = "AWAITING_APPROVAL" if final_state["status"] == "complete" else "NEEDS_HUMAN_TRIAGE"

        incident_created_event = {
            "event_id": str(uuid.uuid4()),
            "incident_id": incident_id,
            "status": incident_status,
            "severity": "HIGH",
            "title": f"Anomalous Activity on {prediction.target_node_id}",
            "summary": final_state["report"].executive_summary if final_state["report"] else "Under triage",
            "model_version": prediction.model_version,
            "timestamp": prediction.timestamp.isoformat()
        }

        remediation_proposal_event = None
        if final_state["proposed_remediation"]:
            rem = final_state["proposed_remediation"]
            remediation_proposal_event = {
                "event_id": str(uuid.uuid4()),
                "incident_id": str(rem.incident_id),
                "action_type": rem.action_type,
                "target": rem.target,
                "risk_level": rem.risk_level,
                "reason": rem.reason,
                "proposed_by": rem.proposed_by,
                "status": rem.status,
                "created_at": rem.created_at.isoformat()
            }

        logger.info(f"Agent pipeline finished processing incident {incident_id}. Status: {incident_status}")
        return {
            "status": final_state["status"],
            "incident_created_event": incident_created_event,
            "remediation_proposal_event": remediation_proposal_event
        }
