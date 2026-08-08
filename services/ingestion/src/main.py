import os
import logging
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from services.ingestion.src.replay import TelemetryReplayEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ingestion_service")

app = FastAPI(
    title="SentinelGraph Telemetry Ingestion Service",
    description="Developer 1 Ingestion Service for raw network/host telemetry",
    version="1.0.0"
)

replay_engine = TelemetryReplayEngine()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ingestion-service"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready", "service": "ingestion-service"}


@app.post("/ingest/event", status_code=202)
def ingest_single_event(payload: Dict[str, Any]):
    event_id = payload.get("event_id")
    if not event_id:
        raise HTTPException(status_code=400, detail="Missing required field 'event_id'")
    logger.info(f"[IngestionService] Ingested event {event_id} from {payload.get('source_host')}")
    return {"status": "accepted", "event_id": event_id}


@app.post("/ingest/replay", status_code=202)
def replay_scenario(count: int = 5):
    events = replay_engine.generate_scenario_stream(count=count)
    logger.info(f"[IngestionService] Replayed scenario stream with {len(events)} events to security.raw.events")
    return {"status": "replayed", "count": len(events), "events": events}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
