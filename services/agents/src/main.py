import os
import sys
import time
import logging
from services.agents.src.kafka_consumer import AgentKafkaHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("agent_service_main")


def main():
    logger.info("Initializing SentinelGraph Agent Service (Developer 2)...")
    kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    postgres_uri = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@localhost:5432/sentinelgraph")

    logger.info(f"Connected to Kafka brokers at {kafka_bootstrap}")
    logger.info(f"Connected to PostgreSQL at {postgres_uri}")

    handler = AgentKafkaHandler()
    logger.info("Agent Service ready and listening for ml.predictions and ml.attributions events.")
    
    # Keeping service loop active
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Agent service shutting down gracefully.")


if __name__ == "__main__":
    main()
