from fastapi import APIRouter
from services.api.src.db import ReadOnlyDatabaseClient

router = APIRouter(prefix="/api/dashboard", tags=["graph"])
db_client = ReadOnlyDatabaseClient()


@router.get("/graph/{incident_id}")
def get_cytoscape_graph(incident_id: str):
    return db_client.get_cytoscape_graph(incident_id)
