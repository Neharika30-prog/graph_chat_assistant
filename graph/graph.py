from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, src, rel, dst):
        self.edges[src].append((rel, dst))

    # ✅ NEW
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    # ✅ NEW
    def add_edges(self, edges):
        for src, rel, dst in edges:
            self.add_edge(src, rel, dst)
    
def owners_of(self, service):
    owners = set()
    for src, relations in self.edges.items():
        for rel, dst in relations:
            if rel == "OWNS" and dst == service:
                owners.add(src)
    return list(owners)
    
    def dependencies_of(self, service):
       deps = []

       for rel, dst in self.edges.get(service, []):
            if rel == "DEPENDS_ON":
                deps.append(dst)

       return deps
    
    def reverse_dependencies(self, service):
      dependents = []

      for src, relations in self.edges.items():
        for rel, dst in relations:
            if rel == "DEPENDS_ON" and dst == service:
                dependents.append(src)

      return dependents


    def print_graph(self):
        print("\nGRAPH:")
        for src, relations in self.edges.items():
            for rel, dst in relations:
                print(f"{src} -[{rel}]-> {dst}")

    

