-- Migration: 001_init_dev1_tables.sql
-- Owner: Developer 1 (Data & ML Platform Engineer)

CREATE TABLE IF NOT EXISTS ml_model_versions (
    version VARCHAR(64) PRIMARY KEY,
    model_type VARCHAR(32) NOT NULL CHECK (model_type IN ('GraphSAGE', 'GAT', 'XGBoost')),
    metrics_json JSONB NOT NULL,
    trained_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_ml_model_versions_active ON ml_model_versions(active);
