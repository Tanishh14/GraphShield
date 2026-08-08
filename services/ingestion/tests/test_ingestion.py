from services.ingestion.src.replay import TelemetryReplayEngine
from services.ingestion.src.main import app


def test_telemetry_replay_engine():
    engine = TelemetryReplayEngine()
    event = engine.generate_raw_event("host-test-01")
    assert "event_id" in event
    assert event["source_host"] == "host-test-01"


def test_scenario_stream():
    engine = TelemetryReplayEngine()
    stream = engine.generate_scenario_stream(count=4)
    assert len(stream) == 4
    assert stream[0]["source_host"] == "host-01"
