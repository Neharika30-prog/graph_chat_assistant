import time
from neo4j import GraphDatabase, exceptions

class GraphStorage:
    def __init__(self):
        uri = "bolt://neo4j:7687"

        for i in range(10):
            try:
                self.driver = GraphDatabase.driver(
                    uri, auth=("neo4j", "password")
                )
                self.session = self.driver.session()
                self.session.run("RETURN 1")
                print("✅ Connected to Neo4j")
                break
            except exceptions.ServiceUnavailable:
                print("⏳ Waiting for Neo4j...")
                time.sleep(3)
        else:
            raise RuntimeError("❌ Neo4j not reachable")