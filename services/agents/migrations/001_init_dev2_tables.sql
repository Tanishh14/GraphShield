-- Migration: 001_init_dev2_tables.sql
-- Owner: Developer 2 (Agent & Intelligence API Layer)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Table: incidents (Owner: agents)
CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(32) NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'INVESTIGATING', 'AWAITING_APPROVAL', 'APPROVED', 'REJECTED', 'CLOSED', 'NEEDS_HUMAN_TRIAGE')),
    gnn_prediction_id UUID,
    severity VARCHAR(16) NOT NULL DEFAULT 'MEDIUM' CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    model_version VARCHAR(64) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_created_at ON incidents(created_at DESC);

-- Table: agent_reports (Owner: agents)
CREATE TABLE IF NOT EXISTS agent_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    agent_type VARCHAR(32) NOT NULL CHECK (agent_type IN ('INVESTIGATION', 'THREAT_INTEL', 'ACTION_REPORT')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    content JSONB NOT NULL,
    grounded BOOLEAN NOT NULL DEFAULT TRUE,
    attribution_refs JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_agent_reports_incident_id ON agent_reports(incident_id);

-- Table: mitre_attack_techniques (Owner: agents)
CREATE TABLE IF NOT EXISTS mitre_attack_techniques (
    technique_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tactic VARCHAR(64) NOT NULL,
    description TEXT,
    url TEXT
);

-- Table: cve_records (Owner: agents)
CREATE TABLE IF NOT EXISTS cve_records (
    cve_id VARCHAR(32) PRIMARY KEY,
    description TEXT NOT NULL,
    cvss_score NUMERIC(3, 1),
    published_at TIMESTAMPTZ,
    source_url TEXT
);

-- Table: kb_documents (Owner: agents / pgvector RAG)
CREATE TABLE IF NOT EXISTS kb_documents (
    doc_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source VARCHAR(32) NOT NULL CHECK (source IN ('MITRE', 'CVE', 'DOC')),
    chunk_text TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Table: kb_embeddings (Owner: agents / pgvector RAG)
CREATE TABLE IF NOT EXISTS kb_embeddings (
    doc_id UUID PRIMARY KEY REFERENCES kb_documents(doc_id) ON DELETE CASCADE,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Cosine similarity ivfflat index for pgvector search
CREATE INDEX IF NOT EXISTS idx_kb_embeddings_vector ON kb_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
