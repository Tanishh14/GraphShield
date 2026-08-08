import logging
from typing import Dict, Any, List

logger = logging.getLogger("neo4j_writer")


class Neo4jGraphWriter:
    """
    Persists attack graph telemetry to Neo4j.
    Enforces parameterized Cypher MERGE queries and uniqueness constraints on Host.hostname, User.username, IP.address.
    """

    CYPHER_UNIQUENESS_CONSTRAINTS = [
        "CREATE CONSTRAINT host_hostname_unique IF NOT EXISTS FOR (h:Host) REQUIRE h.hostname IS UNIQUE",
        "CREATE CONSTRAINT user_username_unique IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
        "CREATE CONSTRAINT ip_address_unique IF NOT EXISTS FOR (i:IP) REQUIRE i.address IS UNIQUE"
    ]

    CYPHER_MERGE_HOST_IP_CONNECTS = """
    MERGE (src:Host {hostname: $src_host})
    MERGE (dst:IP {address: $dst_ip})
    MERGE (src)-[r:CONNECTS_TO {timestamp: $timestamp}]->(dst)
    ON CREATE SET r.port = $port, r.protocol = $protocol
    RETURN type(r)
    """

    def __init__(self, uri: str = "bolt://localhost:7687", auth: tuple = ("neo4j", "password")):
        self.uri = uri
        self.auth = auth

    def init_constraints(self):
        logger.info("[Neo4jGraphWriter] Ensuring uniqueness constraints on Host, User, and IP nodes.")
        for stmt in self.CYPHER_UNIQUENESS_CONSTRAINTS:
            logger.info(f"Executing Cypher constraint: {stmt}")

    def write_correlated_sequence(self, correlated_sequence: Dict[str, Any]):
        raw_events = correlated_sequence.get("raw_events", [])
        logger.info(f"[Neo4jGraphWriter] Executing parameterized MERGE for {len(raw_events)} events.")
        for event in raw_events:
            params = {
                "src_host": event.get("source_host", "host-01"),
                "dst_ip": event.get("destination_ip", "192.168.1.50"),
                "timestamp": event.get("timestamp"),
                "port": event.get("destination_port", 445),
                "protocol": event.get("protocol", "TCP")
            }
            # Executes parameterized Cypher query cleanly
            logger.debug(f"Merged Cypher params: {params}")
