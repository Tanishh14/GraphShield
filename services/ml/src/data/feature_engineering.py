import logging
from typing import Dict, Any, List

logger = logging.getLogger("feature_engineering")


class FlowFeatureEngineer:
    """Feature engineering pipeline for network flow statistics and protocol one-hot encoding."""

    PROTOCOLS = ["TCP", "UDP", "ICMP", "OTHER"]

    @classmethod
    def extract_features(cls, flow: Dict[str, Any]) -> List[float]:
        """Extracts normalized tabular feature vector for flow data."""
        flow_bytes = float(flow.get("flow_bytes_per_sec", 0.0)) / 10000000.0  # Normalized
        packet_count = float(flow.get("packet_count", 0)) / 10000.0
        failed_logins = float(flow.get("failed_login_attempts", 0)) / 10.0

        # One-hot encode protocol
        protocol_str = flow.get("protocol", "TCP").upper()
        one_hot_proto = [1.0 if protocol_str == p else 0.0 for p in cls.PROTOCOLS]

        feature_vector = [flow_bytes, packet_count, failed_logins] + one_hot_proto
        return feature_vector
