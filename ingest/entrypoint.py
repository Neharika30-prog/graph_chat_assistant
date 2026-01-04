from connectors.docker_connector import parse_docker_compose
from connectors.teams_connector import parse_teams
from connectors.k8s_connector import parse_k8s
from graph.storage import GraphStorage

def run_ingestion():
    store = GraphStorage()

    # ---- Docker Compose ----
    nodes, edges = parse_docker_compose("infra/docker-compose.yml")
    store.ingest(nodes, edges)

    # ---- Teams ----
    nodes, edges = parse_teams("infra/teams.yaml")
    store.ingest(nodes, edges)

    # ---- Kubernetes (optional but supported) ----
    try:
     nodes, edges = parse_k8s("infra/k8s.yaml")
     store.ingest(nodes, edges)
    except FileNotFoundError:
     print("⚠️ k8s config not found, skipping")

    print("✅ Graph ingestion complete (docker + teams + k8s)")
    store.close()

if __name__ == "__main__":
    run_ingestion()

