from typing import TypedDict, Optional, Literal
from contracts.schemas.models import (
    GNNPrediction,
    AttributionResult,
    InvestigationResult,
    ThreatIntelResult,
    ActionReportResult,
    ProposedRemediation
)


class AgentState(TypedDict):
    incident_id: str
    prediction: Optional[GNNPrediction]
    attribution: Optional[AttributionResult]
    investigation_result: Optional[InvestigationResult]
    threat_intel_result: Optional[ThreatIntelResult]
    report: Optional[ActionReportResult]
    proposed_remediation: Optional[ProposedRemediation]
    retries: int
    status: Literal["running", "needs_retry", "failed", "complete"]
