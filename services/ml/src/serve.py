import uuid
import logging
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from services.ml.src.models.graphsage import GraphSAGEModel
from services.ml.src.explain.explainer import GNNExplainerEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ml_service_serve")

app = FastAPI(
    title="SentinelGraph ML & Explainability Service",
    description="Developer 1 GNN Model Inference & GNNExplainer Attribution API",
    version="1.0.0"
)

model = GraphSAGEModel()
explainer = GNNExplainerEngine()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ml-service"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready", "service": "ml-service"}


@app.post("/predict")
def predict_and_explain(graph_snapshot: Dict[str, Any]):
    incident_id = uuid.uuid4()
    prediction, confidence, anomaly_score = model.predict(graph_snapshot)

    attribution = None
    if anomaly_score > 0.5:
        attribution = explainer.explain(
            incident_id=incident_id,
            prediction_label=prediction,
            confidence=confidence,
            graph_snapshot=graph_snapshot,
            model_version=model.model_version
        )

    return {
        "incident_id": str(incident_id),
        "prediction": prediction,
        "confidence": confidence,
        "anomaly_score": anomaly_score,
        "attribution": attribution.dict() if attribution else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
