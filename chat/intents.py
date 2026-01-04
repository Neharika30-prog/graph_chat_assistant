from enum import Enum

class Intent(Enum):
    GET_OWNER = "get_owner"
    GET_DEPENDENCIES = "get_dependencies"
    GET_DEPENDENTS = "get_dependents"
    BLAST_RADIUS = "blast_radius"
    LIST_SERVICES = "list_services"
    LIST_DATABASES = "list_databases"
    LIST_TEAMS = "list_teams"
    SHORTEST_PATH = "shortest_path"
    UNKNOWN = "unknown"
