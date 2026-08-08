"""
services/ml/tests/test_temporal_split.py
Owner: Developer 1 (Data & ML Platform Engineer)

Tests temporal train/val/test split to guarantee zero future data leakage.
"""

import pytest
from services.ml.src.data.dataset import TemporalDatasetLoader


def test_temporal_split_no_leakage():
    loader = TemporalDatasetLoader(train_ratio=0.5, val_ratio=0.25, test_ratio=0.25)
    samples = [
        {"id": 1, "timestamp": "2026-08-08T10:00:00Z"},
        {"id": 2, "timestamp": "2026-08-08T11:00:00Z"},
        {"id": 3, "timestamp": "2026-08-08T12:00:00Z"},
        {"id": 4, "timestamp": "2026-08-08T13:00:00Z"},

    ]

    train, val, test = loader.temporal_split(samples)

    assert len(train) == 2
    assert len(val) == 1
    assert len(test) == 1

    # Assert strict chronological ordering
    assert train[-1]["timestamp"] <= val[0]["timestamp"]
    assert val[-1]["timestamp"] <= test[0]["timestamp"]
