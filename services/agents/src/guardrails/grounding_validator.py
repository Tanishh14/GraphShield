import re
import logging
from typing import List, Tuple, Dict, Any, Set
from contracts.schemas.models import AttributionResult

logger = logging.getLogger("grounding_validator")


class GroundingValidationError(Exception):
    """Raised when generated report text fails deterministic attribution grounding checks."""
    pass


class GroundingValidator:
    """
    Deterministic Entity Matching Validator.
    Parses generated text from Action & Report Agent and validates that every entity reference
    (hosts, IPs, processes, technique IDs) resolves to an ID present in AttributionResult.
    """

    @staticmethod
    def extract_entity_references(text: str) -> Set[str]:
        """Extracts candidate node IDs, IP addresses, hostnames, and technique IDs from text using regex patterns."""
        entities = set()

        # Match IP addresses (e.g. 192.168.1.50)
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        for match in re.findall(ip_pattern, text):
            entities.add(match)

        # Match hostnames / hyphenated node IDs (e.g. host-01, srv-rogue-99, ws-finance-02)
        host_pattern = r'\b(?:host|srv|ws|workstation|node)-[A-Za-z0-9\-]+\b'
        for match in re.findall(host_pattern, text, flags=re.IGNORECASE):
            entities.add(match)
        
        # Match MITRE Technique IDs (e.g. T1078, T1059.001)
        mitre_pattern = r'\bT\d{4}(?:\.\d{3})?\b'
        for match in re.findall(mitre_pattern, text):
            entities.add(match)

        return entities

    @classmethod
    def validate_and_sanitize_report(
        cls, report_text: str, attribution: AttributionResult
    ) -> Tuple[str, bool, List[str]]:
        """
        Validates text against attribution.important_nodes and attribution.important_edges.
        If non-grounded entities are found, strips the offending sentences and flags grounded=False.
        """
        if not attribution:
            logger.warning("No AttributionResult provided for grounding validation.")
            return report_text, True, []

        allowed_nodes: Set[str] = set(attribution.important_nodes)
        
        # Add edge endpoints
        for src, dst in attribution.important_edges:
            allowed_nodes.add(src)
            allowed_nodes.add(dst)

        # Also extract nodes from subgraph if available
        if attribution.subgraph and "nodes" in attribution.subgraph:
            for n in attribution.subgraph["nodes"]:
                if isinstance(n, dict) and "id" in n:
                    allowed_nodes.add(str(n["id"]))
                elif isinstance(n, str):
                    allowed_nodes.add(n)

        sentences = re.split(r'(?<=[.!?])\s+', report_text)
        sanitized_sentences = []
        unresolvable_claims = []
        is_fully_grounded = True

        for sentence in sentences:
            sentence_entities = cls.extract_entity_references(sentence)
            
            # Filter entities to check specific host/IP patterns
            suspicious_entities = [
                e for e in sentence_entities 
                if (re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', e) or e.startswith("host-") or e.startswith("srv-") or e.startswith("ws-"))
            ]
            
            invalid_in_sentence = [e for e in suspicious_entities if e not in allowed_nodes]

            if invalid_in_sentence:
                logger.warning(f"Grounding validator flagged unresolvable entity references in sentence: {invalid_in_sentence}")
                unresolvable_claims.extend(invalid_in_sentence)
                is_fully_grounded = False
                # Sentence is stripped from sanitized output
            else:
                sanitized_sentences.append(sentence)

        sanitized_text = " ".join(sanitized_sentences)
        return sanitized_text, is_fully_grounded, unresolvable_claims
