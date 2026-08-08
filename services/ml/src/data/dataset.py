import logging
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

logger = logging.getLogger("dataset_temporal_split")


class TemporalDatasetLoader:
    """
    Enforces a strict Temporal Train/Val/Test Split for CICIDS2018 flow data.
    Never uses random splitting, ensuring zero future data leakage backward into training.
    """

    def __init__(self, train_ratio: float = 0.6, val_ratio: float = 0.2, test_ratio: float = 0.2):
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio

    def temporal_split(self, samples: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Sorts samples by timestamp and partitions chronologically into train, val, test."""
        # Sort chronologically by timestamp
        sorted_samples = sorted(samples, key=lambda x: x.get("timestamp", "2026-08-08T00:00:00Z"))

        n = len(sorted_samples)
        train_end = int(n * self.train_ratio)
        val_end = train_end + int(n * self.val_ratio)

        train_set = sorted_samples[:train_end]
        val_set = sorted_samples[train_end:val_end]
        test_set = sorted_samples[val_end:]

        # Assert no temporal leakage
        if train_set and val_set:
            max_train_time = max(x["timestamp"] for x in train_set)
            min_val_time = min(x["timestamp"] for x in val_set)
            assert max_train_time <= min_val_time, f"Temporal Leakage Detected! max_train ({max_train_time}) > min_val ({min_val_time})"

        if val_set and test_set:
            max_val_time = max(x["timestamp"] for x in val_set)
            min_test_time = min(x["timestamp"] for x in test_set)
            assert max_val_time <= min_test_time, f"Temporal Leakage Detected! max_val ({max_val_time}) > min_test ({min_test_time})"

        logger.info(f"[TemporalDatasetLoader] Split dataset chronologically: {len(train_set)} train, {len(val_set)} val, {len(test_set)} test.")
        return train_set, val_set, test_set
