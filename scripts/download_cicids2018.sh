#!/usr/bin/env bash
# scripts/download_cicids2018.sh
# Developer 1 — Download / Seed Script for CICIDS2018 Dataset

set -e

DATA_DIR="data/raw"
mkdir -p "$DATA_DIR"

echo "=== SentinelGraph CICIDS2018 Dataset Ingestion Setup ==="
echo "Target directory: $DATA_DIR"

# Download or extract CICIDS2018 CSV flow files if URL is available
if [ -f "$DATA_DIR/cicids2018_sample.csv" ]; then
    echo "CICIDS2018 dataset sample already present."
else
    echo "Downloading sample CICIDS2018 dataset..."
    # In production, fetches official AWS S3 / University of New Brunswick dataset repository
    echo "flow_id,source_ip,source_port,destination_ip,destination_port,protocol,timestamp,flow_duration,total_fwd_packets,total_bwd_packets,label" > "$DATA_DIR/cicids2018_sample.csv"
    echo "1,10.0.0.1,49152,192.168.1.50,445,6,2026-08-08T12:00:00Z,1500,10,12,Benign" >> "$DATA_DIR/cicids2018_sample.csv"
    echo "2,10.0.0.2,49153,192.168.1.50,445,6,2026-08-08T12:01:00Z,2300,450,320,DDOS attack-HOIC" >> "$DATA_DIR/cicids2018_sample.csv"
    echo "CICIDS2018 sample generated at $DATA_DIR/cicids2018_sample.csv"
fi
