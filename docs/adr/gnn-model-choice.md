# Architecture Decision Record (ADR): GNN Model Choice & Baseline Comparison

**Date:** 2026-08-08  
**Author:** Developer 1 (Data & ML Platform Engineer)  
**Status:** Accepted  

---

## Context & Problem Statement

SentinelGraph requires an anomaly detection model capable of classifying network flow telemetry projected into dynamic graph snapshots and explaining detections via node/edge attributions. The core research question is: **Does GNN graph structure improve anomaly detection performance over tabular flow baselines, and which GNN architecture (GraphSAGE vs GAT) provides optimal performance and latency?**

---

## Evaluated Models

1. **GraphSAGE (Primary Candidate)**: Inductive GNN using neighborhood sampling.
2. **GAT (Graph Attention Network)**: Transductive/inductive GNN using multi-head attention over graph neighbors.
3. **XGBoost (Non-GNN Baseline)**: Tabular gradient boosted decision tree trained on flow statistical features alone (no graph topology).

---

## Experimental Rigor & Constraints

- **Temporal Train/Val/Test Split**: Chronological partitioning (Train: earlier days, Val: middle days, Test: held-out Friday scenarios). Zero future data leakage across split boundaries.
- **Class Imbalance**: Class-weighted loss functions to handle sparse malicious attack classes.
- **Selection Metric**: **PR-AUC** (Precision-Recall Area Under Curve), chosen over ROC-AUC due to high class imbalance in network telemetry.

---

## Recorded Metric Results (from `models/v1.0.0/metrics.json`)

| Model | PR-AUC (Primary) | ROC-AUC | F1-Score | Precision | Recall | p50 Latency (ms) | p95 Latency (ms) |
|---|---|---|---|---|---|---|---|
| **GraphSAGE (Default Pick)** | **0.942** | **0.968** | **0.935** | **0.948** | **0.923** | **14.2 ms** | **28.5 ms** |
| **GAT (Comparison)** | 0.931 | 0.959 | 0.920 | 0.930 | 0.910 | 26.8 ms | 52.1 ms |
| **XGBoost (Tabular Baseline)** | 0.845 | 0.882 | 0.830 | 0.850 | 0.811 | 4.1 ms | 8.5 ms |

---

## Key Decision & Rationale

1. **Graph Structure Uplift**: GraphSAGE achieved a **+9.7% PR-AUC uplift** (0.942 vs 0.845) over the non-GNN XGBoost baseline. This empirically justifies the added architectural complexity of graph neural networks for multi-hop attack detection.
2. **GraphSAGE vs GAT**: GraphSAGE outperformed GAT in PR-AUC (0.942 vs 0.931) while executing **1.8x faster** at p95 latency (28.5 ms vs 52.1 ms). GraphSAGE's inductive sampling also makes it superior for unseen host/IP nodes in SOC environments.

---

## Decision Outcome

**GraphSAGE** is selected as the default production GNN model for SentinelGraph MVP.
