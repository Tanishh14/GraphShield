from datetime import datetime
from typing import Literal, Optional, Any, Dict, List, Tuple
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class GNNPrediction(BaseModel):
    incident_candidate_id: UUID = Field(default_factory=uuid4)
    model_version: str
    prediction: Literal["benign", "anomalous"]
    confidence: float = Field(ge=0.0, le=1.0)
    anomaly_score: float = Field(ge=0.0, le=1.0)
    target_node_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AttributionResult(BaseModel):
    incident_id: UUID
    model_version: str
    prediction: Literal["benign", "anomalous"]
    confidence: float = Field(ge=0.0, le=1.0)
    important_nodes: List[str]
    important_edges: List[Tuple[str, str]]
    important_features: Dict[str, float]
    subgraph: Dict[str, Any]  # Node-link format representation for Cytoscape


class InvestigationResult(BaseModel):
    incident_id: UUID
    summary: str
    affected_entities: List[str]
    attack_path: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    correlation_notes: str


class ThreatIntelResult(BaseModel):
    incident_id: UUID
    retrieved_evidence: List[Dict[str, Any]]  # List of chunks with doc_id and source_url citations
    interpretation: str
    matched_techniques: List[str]
    matched_cves: List[str]


class ActionReportResult(BaseModel):
    incident_id: UUID
    executive_summary: str
    risk_assessment: str
    detailed_findings: str
    grounded: bool = True
    attribution_refs: List[str] = Field(default_factory=list)


class ProposedRemediation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    incident_id: UUID
    action_type: Literal["ISOLATE_HOST", "DISABLE_USER", "BLOCK_IP", "TERMINATE_PROCESS"]
    target: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    reason: str
    proposed_by: str = "ActionReportAgent"
    status: Literal["PROPOSED", "APPROVED", "REJECTED", "EXECUTED", "FAILED"] = "PROPOSED"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Incident(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["OPEN", "INVESTIGATING", "AWAITING_APPROVAL", "APPROVED", "REJECTED", "CLOSED", "NEEDS_HUMAN_TRIAGE"] = "OPEN"
    gnn_prediction_id: Optional[UUID] = None
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"
    title: str
    summary: str
    model_version: str


class AgentState(BaseModel):
    incident_id: str
    prediction: Optional[GNNPrediction] = None
    attribution: Optional[AttributionResult] = None
    investigation_result: Optional[InvestigationResult] = None
    threat_intel_result: Optional[ThreatIntelResult] = None
    report: Optional[ActionReportResult] = None
    proposed_remediation: Optional[ProposedRemediation] = None
    retries: int = 0
    status: Literal["running", "needs_retry", "failed", "complete"] = "running"
