from graph.query import GraphQueryEngine
from chat.intents import Intent

class QueryDispatcher:
    def __init__(self, query_engine: GraphQueryEngine):
        self.q = query_engine

    def dispatch(self, intent, params):
        if intent == Intent.GET_OWNER:
            return self.q.get_owner(params["node"])

        if intent == Intent.GET_DEPENDENCIES:
            return self.q.downstream(params["node"])

        if intent == Intent.GET_DEPENDENTS:
            return self.q.upstream(params["node"])

        if intent == Intent.BLAST_RADIUS:
            return self.q.blast_radius(params["node"])

        if intent == Intent.SHORTEST_PATH:
            return self.q.path(params["from"], params["to"])

        if intent == Intent.LIST_SERVICES:
            return self.q.get_nodes("Service")

        if intent == Intent.LIST_DATABASES:
            return self.q.get_nodes("Database")

        if intent == Intent.LIST_TEAMS:
            return self.q.get_nodes("Team")
        
        if intent == "LIST_SERVICES":
            return self.engine.list_services()

        if intent == "LIST_DATABASES":
            return self.engine.list_databases()

        if intent == "LIST_TEAMS":
            return self.engine.list_teams()

        return None
