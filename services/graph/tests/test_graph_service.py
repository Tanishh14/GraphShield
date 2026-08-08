from services.graph.src.neo4j_writer import Neo4jGraphWriter
from services.graph.src.pyg_builder import PyGGraphSnapshotBuilder


def test_neo4j_graph_writer_constraints():
    writer = Neo4jGraphWriter()
    writer.init_constraints()
    assert len(writer.CYPHER_UNIQUENESS_CONSTRAINTS) == 3


def test_pyg_snapshot_builder():
    builder = PyGGraphSnapshotBuilder()
    seq = {
        "raw_events": [
            {"source_host": "host-01", "destination_ip": "192.168.1.50"}
        ]
    }
    snapshot = builder.create_in_memory_snapshot(seq)
    assert snapshot["num_nodes"] == 2
    assert snapshot["num_edges"] == 1
    assert "pyg_tensors" in snapshot
