class GraphQueryEngine:
    def __init__(self, storage):
        self.storage = storage
        self.session = storage.session

    def get_node(self, node_id):
     result = self.session.run(
        """
        MATCH (n {id: $id})
        RETURN labels(n) AS labels, n.id AS id, properties(n) AS props
        """,
        id=node_id
     )
     return result.single()
    
    def get_nodes(self, node_type, filters=None):
     filters = filters or {}
     where_clause = " AND ".join([f"n.{k} = ${k}" for k in filters])

     query = f"""
     MATCH (n:{node_type})
     {f"WHERE {where_clause}" if where_clause else ""}
     RETURN n.id AS id, properties(n) AS props
     """

     return list(self.session.run(query, **filters))
 
    def downstream(self, node_id, edge_types=None):
     rels = edge_types or ["DEPENDS_ON", "CALLS", "STORES_DATA_IN"]
     rel_filter = "|".join(rels)

     result = self.session.run(
        f"""
        MATCH (n {{id: $id}})-[:{rel_filter}*]->(d)
        RETURN DISTINCT d.id AS id
        """,
        id=node_id
    )
     return [r["id"] for r in result]


    def upstream(self, node_id, edge_types=None):
     rels = edge_types or ["DEPENDS_ON", "CALLS", "STORES_DATA_IN"]
     rel_filter = "|".join(rels)

     result = self.session.run(
        f"""
        MATCH (u)-[:{rel_filter}*]->(n {{id: $id}})
        RETURN DISTINCT u.id AS id
        """,
        id=node_id
    )
     return [r["id"] for r in result]
   
    def blast_radius(self, node_id):
     result = self.session.run(
        """
        MATCH (n {id: $id})
        OPTIONAL MATCH (n)-[:DEPENDS_ON|CALLS|STORES_DATA_IN*]->(down)
        OPTIONAL MATCH (up)-[:DEPENDS_ON|CALLS|STORES_DATA_IN*]->(n)
        OPTIONAL MATCH (t:Team)-[:OWNS]->(n)
        RETURN DISTINCT down.id AS down, up.id AS up, t.id AS team
        """,
        id=node_id
     )

     affected = set()
     teams = set()

     for r in result:
        if r["down"]:
            affected.add(r["down"])
        if r["up"]:
            affected.add(r["up"])
        if r["team"]:
            teams.add(r["team"])

     affected.discard(node_id)

     return {
        "affected_nodes": list(affected),
        "affected_teams": list(teams)
    }



    def path(self, from_id, to_id):
     result = self.session.run(
        """
        MATCH p = shortestPath(
            (a {id: $from_id})-[:DEPENDS_ON|CALLS|STORES_DATA_IN*]-(b {id: $to_id})
        )
        RETURN [n IN nodes(p) | n.id] AS path
        """,
        from_id=from_id,
        to_id=to_id
    )

     record = result.single()
     return record["path"] if record else []
    

    def get_owner(self, node_id):
     result = self.session.run(
        """
        MATCH (s {id: $id})<-[:OWNS]-(t:Team)
        RETURN DISTINCT t.id AS team

        """,
        id=node_id
    )
     return [r["team"] for r in result]
     def list_services(self):
        result = self.session.run(
            """
            MATCH (s:Service)
            RETURN DISTINCT s.id AS service
            ORDER BY service
            """
        )
        return [r["service"] for r in result]

    def list_databases(self):
        result = self.session.run(
            """
            MATCH (d:Database)
            RETURN DISTINCT d.id AS database
            ORDER BY database
            """
        )
        return [r["database"] for r in result]

    def list_teams(self):
        result = self.session.run(
            """
            MATCH (t:Team)
            RETURN DISTINCT t.id AS team
            ORDER BY team
            """
        )
        return [r["team"] for r in result]
