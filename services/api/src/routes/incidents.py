from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.api.src.db import ReadOnlyDatabaseClient

router = APIRouter(prefix="/api/incidents", tags=["incidents"])
db_client = ReadOnlyDatabaseClient()


@router.get("")
def list_incidents(status: Optional[str] = None, limit: int = Query(20, ge=1, le=100)):
    return db_client.get_incidents(status=status, limit=limit)


@router.get("/{incident_id}")
def get_incident_detail(incident_id: str):
    data = db_client.get_incident_detail(incident_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")
    return data
