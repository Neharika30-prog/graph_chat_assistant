import os
import time 
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class GraphStorage:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")

        # Retry logic starts here
        while True:
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
                # This line forces a check to see if the DB is actually responding
                self.driver.verify_connectivity() 
                print("✅ Successfully connected to Neo4j!")
                break
            except ServiceUnavailable:
                print("⏳ Neo4j is not ready yet. Retrying in 5 seconds...")
                time.sleep(5)

        self.session = self.driver.session()

    def upsert_node(self, label, node_id, props=None):
        if props is None:
            props = {}

        query = f"""
        MERGE (n:{label} {{id: $id}})
        SET n += $props
        """
        self.session.run(query, id=node_id, props=props)


    def upsert_edge(self, src_label, src_id, rel_type, dst_label, dst_id):
        query = f"""
        MATCH (a:{src_label} {{id: $src_id}})
        MATCH (b:{dst_label} {{id: $dst_id}})
        MERGE (a)-[:{rel_type}]->(b)
        """
        self.session.run(query, src_id=src_id, dst_id=dst_id)

    def ingest(self, nodes, edges):
    # ---- upsert nodes ----
       for node in nodes:
         if len(node) == 2:
            node_type, node_id = node
            props = {}
         elif len(node) == 3:
            node_type, node_id, props = node
         else:
            raise ValueError(f"Invalid node format: {node}")

         self.upsert_node(node_type, node_id, props)

    # ---- upsert edges ----
       for edge in edges:
          if len(edge) == 3:
            src_id, rel_type, dst_id = edge
            # default assumption: Service -> Service
            self.upsert_edge(
                "Service", src_id,
                rel_type,
                "Service", dst_id
            )

          elif len(edge) == 5:
            src_label, src_id, rel_type, dst_label, dst_id = edge
            self.upsert_edge(
                src_label, src_id,
                rel_type,
                dst_label, dst_id
            )

          else:
            raise ValueError(f"Invalid edge format: {edge}")

    def owners_of(self, service):
        result = self.session.run(
            """
            MATCH (t:Team)-[:OWNS]->(s:Service {id: $service})
            RETURN t.id AS team
            """,
            service=service
        )
        return [r["team"] for r in result]

    def dependencies_of(self, service):
        result = self.session.run(
            """
            MATCH (s:Service {id: $service})
                  -[:DEPENDS_ON|CALLS|STORES_DATA_IN]->(d)
            RETURN d.id AS dep
            """,
            service=service
        )
        return list(set(r["dep"] for r in result))

    def reverse_dependencies(self, target):
        result = self.session.run(
            """
            MATCH (s)-[:DEPENDS_ON|CALLS|STORES_DATA_IN]->(t {id: $target})
            RETURN s.id AS service
            """,
            target=target
        )
        return list(set(r["service"] for r in result))

    def dependents_of(self, service_name: str):
        query = """
        MATCH (s:Service)-[:DEPENDS_ON]->(d:Service {id: $id})
        RETURN s.id AS dependent
        """
        result = self.session.run(query, id=service_name)
        return [r["dependent"] for r in result]
    
    def blast_radius(self, service_id):
     result = self.session.run(
        """
        MATCH (s:Service {id:$service})-[:DEPENDS_ON*1..3]->(d)
        RETURN DISTINCT d.id AS impacted
        """,
        service=service_id
     )
     return [r["impacted"] for r in result]
    
    def derive_service_ownership(self):
        self.session.run(
            """
            MATCH (team:Team)-[:OWNS]->(db)
            MATCH (service:Service)-[:STORES_DATA_IN]->(db)
            MERGE (team)-[:OWNS]->(service)
            """
        )
    def list_nodes_by_label(self, label):
      """Generic exploration query to find all nodes of a specific type."""
      query = f"MATCH (n:{label}) RETURN n.id AS id"
      result = self.session.run(query)
      return [record["id"] for record in result]

    def get_all_services(self):
      return self.list_nodes_by_label("Service")

    def get_all_databases(self):
     return self.list_nodes_by_label("Database")

    def get_all_teams(self):
      return self.list_nodes_by_label("Team")
    
    def close(self):
        self.session.close()
        self.driver.close()
