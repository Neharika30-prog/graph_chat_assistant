import yaml

def parse_k8s(path):
    nodes = []
    edges = []

    with open(path) as f:
        docs = yaml.safe_load_all(f)

        for doc in docs:
            if doc and doc.get("kind") == "Deployment":
                name = doc["metadata"]["name"]
                nodes.append(("Service", name))
                nodes.append(("Infrastructure", "Kubernetes"))
                edges.append((name, "DEPLOYED_ON", "Kubernetes"))

    return nodes, edges
