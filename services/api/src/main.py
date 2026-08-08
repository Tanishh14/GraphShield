import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.api.src.routes import incidents, graph, health

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="SentinelGraph Intelligence Read API",
    description="Developer 2 Read-Only API layer for SOC Dashboard visualization",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(incidents.router)
app.include_router(graph.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
