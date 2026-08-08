"""
services/ml/tests/test_model_metrics.py
Owner: Developer 1 (Data & ML Platform Engineer)

Regression test checking that recorded metrics.json exists and satisfies performance thresholds.
"""

import os
import json


def test_recorded_metrics_exist_and_pass_threshold():
    metrics_path = "models/v1.0.0/metrics.json"
    assert os.path.exists(metrics_path), f"metrics.json missing at {metrics_path}"

    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    assert "GraphSAGE" in metrics
    assert "PR_AUC" in metrics["GraphSAGE"]

    graphsage_pr_auc = metrics["GraphSAGE"]["PR_AUC"]
    xgboost_pr_auc = metrics["XGBoost_Baseline"]["PR_AUC"]

    # Assert GNN outperforms tabular baseline by at least +0.05 PR-AUC
    assert graphsage_pr_auc > xgboost_pr_auc + 0.05, f"GraphSAGE PR-AUC ({graphsage_pr_auc}) did not significantly beat XGBoost ({xgboost_pr_auc})"
