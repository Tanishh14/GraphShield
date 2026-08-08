from services.correlation.src.correlator import WindowedEventCorrelator


def test_windowed_event_correlator():
    correlator = WindowedEventCorrelator()
    raw_event = {"source_host": "host-01", "event_type": "FLOW", "failed_login_attempts": 4}
    res = correlator.add_event(raw_event)

    assert res["entity_group_id"] == "host-01"
    assert res["events_count"] == 1
    assert res["correlation_metadata"]["anomaly_flag"] is True
