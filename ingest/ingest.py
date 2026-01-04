import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from graph.storage import GraphStorage
from Connectors.docker_connector import parse_docker_compose
from Connectors.teams_connector import parse_teams
from Connectors.k8s_connector import parse_k8s

store = GraphStorage()


def ingest(nodes, edges):
    # upsert nodes
    for node in nodes:
        if len(node) == 2:
            node_type, node_id = node
            props = {}
        elif len(node) == 3:
            node_type, node_id, props = node
        else:
            raise ValueError(f"Invalid node format: {node}")

        store.upsert_node(node_type, node_id, props)
    # upsert edges
    for edge in edges:
        if len(edge) == 3:
            src_id, rel_type, dst_id = edge
            src_label = "Service"
            dst_label = "Service"

        elif len(edge) == 5:
            src_label, src_id, rel_type, dst_label, dst_id = edge

        else:
            raise ValueError(f"Invalid edge format: {edge}")

        store.upsert_edge(src_label, src_id, rel_type, dst_label, dst_id)


# Docker connector
nodes, edges = parse_docker_compose("infra/docker-compose.yml")
ingest(nodes, edges)

# Teams connector
nodes, edges = parse_teams("infra/teams.yaml")
ingest(nodes, edges)

# Kubernetes connector (bonus)
nodes, edges = parse_k8s("infra/k8s-deployments.yaml")
ingest(nodes, edges)

# derive service ownership AFTER all ingestions
store.derive_service_ownership()

print("✅ Graph persisted to Neo4j")

print("\nOWNERS OF payment-service:")
print(store.owners_of("payment-service"))

print("\nDEPENDENCIES OF order-service:")
print(store.dependencies_of("order-service"))

print("\nSERVICES DEPENDING ON redis-main:")
print(store.reverse_dependencies("redis-main"))

print("\nBLAST RADIUS FOR order-service:")
print(store.blast_radius("order-service"))





store.close()
