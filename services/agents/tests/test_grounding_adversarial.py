"""
services/agents/tests/test_grounding_adversarial.py
Owner: Developer 2 (Agent & Intelligence API Engineer)

Adversarial Grounding Validator Test Suite.
Verifies that hallucinated or unresolvable entity references in LLM text are detected and stripped.
"""

import pytest
import uuid
from contracts.schemas.models import AttributionResult
from services.agents.src.guardrails.grounding_validator import GroundingValidator


@pytest.fixture
def sample_attribution():
    return AttributionResult(
        incident_id=uuid.uuid4(),
        model_version="graphsage-v1.0.0",
        prediction="anomalous",
        confidence=0.95,
        important_nodes=["host-01", "192.168.1.50"],
        important_edges=[("host-01", "192.168.1.50")],
        important_features={"flow_bytes": 0.9},
        subgraph={"nodes": [{"id": "host-01"}, {"id": "192.168.1.50"}]}
    )


def test_adversarial_case_1_fabricated_host(sample_attribution):
    """Adversarial Test 1: Injected fabricated hostname 'srv-rogue-99'."""
    raw_text = "Host host-01 communicated with 192.168.1.50. Host srv-rogue-99 was also compromised."
    sanitized, grounded, unresolvable = GroundingValidator.validate_and_sanitize_report(raw_text, sample_attribution)

    assert not grounded
    assert "srv-rogue-99" in unresolvable
    assert "srv-rogue-99" not in sanitized
    assert "host-01" in sanitized


def test_adversarial_case_2_fabricated_ip(sample_attribution):
    """Adversarial Test 2: Injected fabricated IP address '10.99.99.99'."""
    raw_text = "Lateral movement observed from host-01 to 10.99.99.99 during attack execution."
    sanitized, grounded, unresolvable = GroundingValidator.validate_and_sanitize_report(raw_text, sample_attribution)

    assert not grounded
    assert "10.99.99.99" in unresolvable
    assert "10.99.99.99" not in sanitized


def test_adversarial_case_3_valid_grounded_text(sample_attribution):
    """Adversarial Test 3: Completely valid grounded text."""
    raw_text = "Host host-01 initiated network connection to 192.168.1.50."
    sanitized, grounded, unresolvable = GroundingValidator.validate_and_sanitize_report(raw_text, sample_attribution)

    assert grounded
    assert len(unresolvable) == 0
    assert sanitized == raw_text
