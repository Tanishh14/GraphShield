import os
import sys
import time
import logging
from services.graph.src.neo4j_writer import Neo4jGraphWriter
from services.graph.src.pyg_builder import PyGGraphSnapshotBuilder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("graph_service_main")


def main():
    logger.info("Initializing SentinelGraph Graph Service (Developer 1)...")
    neo4j_writer = Neo4jGraphWriter()
    snapshot_builder = PyGGraphSnapshotBuilder()

    neo4j_writer.init_constraints()
    logger.info("Graph Service listening for security.correlated.sequences events.")

    # Service execution loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Graph service shutting down.")


if __name__ == "__main__":
    main()
