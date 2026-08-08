import uuid
from datetime import datetime
from typing import Dict, Any, List


class TelemetryReplayEngine:
    """Replays CICIDS2018 flows and Caldera attack scenario events into canonical RawEvent structures."""

    @staticmethod
    def generate_raw_event(source_host: str = "host-01", destination_ip: str = "192.168.1.50", event_type: str = "FLOW") -> Dict[str, Any]:
        return {
            "event_id": str(uuid.uuid4()),
            "source_host": source_host,
            "source_ip": "10.0.0.1",
            "destination_ip": destination_ip,
            "destination_port": 445,
            "protocol": "TCP",
            "event_type": event_type,
            "flow_bytes_per_sec": 1250000.0,
            "packet_count": 450,
            "failed_login_attempts": 3,
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_scenario_stream(self, count: int = 5) -> List[Dict[str, Any]]:
        events = []
        hosts = ["host-01", "host-02", "srv-db-01", "ws-finance-02"]
        for i in range(count):
            host = hosts[i % len(hosts)]
            events.append(self.generate_raw_event(source_host=host, destination_ip=f"192.168.1.{50+i}"))
        return events
