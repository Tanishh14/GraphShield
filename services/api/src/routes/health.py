from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "api-service"}


@router.get("/ready")
def readiness_check():
    return {"status": "ready", "service": "api-service"}
