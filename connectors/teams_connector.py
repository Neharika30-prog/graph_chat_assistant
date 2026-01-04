import yaml

def parse_teams(path):
    with open(path) as f:
        data = yaml.safe_load(f)

    nodes = []
    edges = []

    if "teams" not in data:
        return [], []

    for team in data["teams"]:
        team_name = team["name"]

        # Team node
        nodes.append(("Team", team_name))

        for owned in team.get("owns", []):
            # Database node
            nodes.append(("Database", owned))

            # Team -> Database ownership
            edges.append(
                ("Team", team_name, "OWNS", "Database", owned)
            )

    return nodes, edges

