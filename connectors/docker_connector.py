import yaml
import re

def parse_docker_compose(path):
    with open(path) as f:
        data = yaml.safe_load(f)

    nodes = []
    edges = []
    services = data.get("services", {})
    if not services:
     return [], []

    for service_name, config in services.items():
        # Service node
        nodes.append(("Service", service_name))

        # Team & oncall
        labels = config.get("labels", {})
        team = labels.get("team")
        oncall = labels.get("oncall")

        if team:
            nodes.append(("Team", team))
            edges.append((team, "OWNS", service_name))

        if oncall:
            nodes.append(("Engineer", oncall))
            edges.append((oncall, "ON_CALL_FOR", service_name))

        # Dependencies
        for dep in config.get("depends_on", []):
         if dep.endswith("-db") or dep.endswith("db") or "redis" in dep:
          nodes.append(("Database", dep))
          edges.append(("Service", service_name, "STORES_DATA_IN", "Database", dep))
        else:
          edges.append(("Service", service_name, "DEPENDS_ON", "Service", dep))
        # Environment variables
        for env in config.get("environment", []):
            if "DATABASE_URL" in env:
                db = re.findall(r'@([^:]+):', env)[0]
                nodes.append(("Database", db))
                edges.append(
                    ("Service", service_name, "STORES_DATA_IN", "Database", db)
                )

            if "_SERVICE_URL" in env:
                target = re.findall(r'http://([^:]+)', env)[0]
                edges.append((service_name, "CALLS", target))

    return nodes, edges
