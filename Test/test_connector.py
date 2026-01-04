from Connectors.docker_connector import parse_docker_compose
from graph import Graph


nodes, edges = parse_docker_compose("infra/docker-compose.yml")

g = Graph()

for n in nodes:
    g.add_node(n)

for src, rel, dst in edges:
    g.add_edge(src, rel, dst)

g.print_graph()
