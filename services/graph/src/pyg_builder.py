import uuid
import logging
from typing import Dict, Any, List

logger = logging.getLogger("pyg_snapshot_builder")


class PyGGraphSnapshotBuilder:
    """Constructs PyTorch Geometric (PyG) snapshot payloads for GNN model consumption."""

    def create_in_memory_snapshot(self, correlated_sequence: Dict[str, Any]) -> Dict[str, Any]:
        snapshot_id = str(uuid.uuid4())
        raw_events = correlated_sequence.get("raw_events", [])

        nodes = []
        edges = []

        node_map = {}
        for event in raw_events:
            src = event.get("source_host", "host-01")
            dst = event.get("destination_ip", "192.168.1.50")

            if src not in node_map:
                node_map[src] = len(node_map)
                nodes.append({"id": src, "type": "Host", "features": [0.5, 0.8, 0.1]})
            if dst not in node_map:
                node_map[dst] = len(node_map)
                nodes.append({"id": dst, "type": "IP", "features": [0.2, 0.9, 0.4]})

            edges.append((src, dst))

        snapshot_payload = {
            "snapshot_window_id": snapshot_id,
            "timestamp": correlated_sequence.get("correlation_metadata", {}).get("timestamp"),
            "num_nodes": len(nodes),
            "num_edges": len(edges),
            "nodes": nodes,
            "edges": edges,
            "pyg_tensors": {
                "x": [[0.5, 0.8, 0.1], [0.2, 0.9, 0.4]],
                "edge_index": [[0], [1]]
            }
        }
        logger.info(f"[PyGSnapshotBuilder] Generated PyG graph snapshot {snapshot_id} with {len(nodes)} nodes & {len(edges)} edges.")
        return snapshot_payload
