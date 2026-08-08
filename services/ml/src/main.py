import os
import sys
import time
import uuid
import logging
from services.ml.src.models.graphsage import GraphSAGEModel
from services.ml.src.explain.explainer import GNNExplainerEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("ml_service_main")


def main():
    logger.info("Initializing SentinelGraph ML Service (Developer 1)...")
    model = GraphSAGEModel()
    explainer = GNNExplainerEngine()

    logger.info(f"Loaded model version {model.model_version}. Listening for graph.snapshots events.")

    # Service execution loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("ML service shutting down.")


if __name__ == "__main__":
    main()
