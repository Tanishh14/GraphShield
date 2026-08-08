import os
import sys
import time
import logging
from services.correlation.src.correlator import WindowedEventCorrelator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("correlation_service_main")


def main():
    logger.info("Initializing SentinelGraph Correlation Service (Developer 1)...")
    correlator = WindowedEventCorrelator(window_size_seconds=300)
    logger.info("Correlation Service ready and listening for security.raw.events.")

    # Service execution loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Correlation service shutting down.")


if __name__ == "__main__":
    main()
