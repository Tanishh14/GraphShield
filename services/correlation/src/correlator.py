import uuid
import logging
from typing import Dict, Any, List

logger = logging.getLogger("event_correlator")


class WindowedEventCorrelator:
    """Windowed Correlation Engine grouping raw telemetry events into correlated behavioral sequences."""

    def __init__(self, window_size_seconds: int = 300):
        self.window_size = window_size_seconds
        self.event_buffers: Dict[str, List[Dict[str, Any]]] = {}

    def add_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        group_key = raw_event.get("source_host", "default_group")
        if group_key not in self.event_buffers:
            self.event_buffers[group_key] = []

        self.event_buffers[group_key].append(raw_event)
        
        # When buffer accumulates threshold events or window closes, emit CorrelationResult
        correlated_sequence = {
            "event_id": str(uuid.uuid4()),
            "entity_group_id": group_key,
            "sequence_id": str(uuid.uuid4()),
            "events_count": len(self.event_buffers[group_key]),
            "raw_events": self.event_buffers[group_key],
            "correlation_metadata": {
                "source_host": group_key,
                "window_size": self.window_size,
                "anomaly_flag": any(e.get("failed_login_attempts", 0) > 2 for e in self.event_buffers[group_key])
            }
        }
        return correlated_sequence
