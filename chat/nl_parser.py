import re
from chat.intents import Intent

def extract_entity(text):
    patterns = [
        r"\b[a-z0-9\-]+-service\b",
        r"\b[a-z0-9\-]+-db\b",
        r"\bredis-main\b",
        r"\b[a-z0-9\-]+-team\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def parse_query(text: str):
    # print("🧪 PARSER INPUT:", text)
    text = text.lower().strip()

    # Ownership
    if "who owns" in text:
        node = extract_entity(text)
        return Intent.GET_OWNER, {"node": node} if node else (Intent.UNKNOWN, {})

    # Dependencies
    if "depend on" in text:
        node = extract_entity(text)
        return Intent.GET_DEPENDENCIES, {"node": node} if node else (Intent.UNKNOWN, {})

    if "uses redis" in text or "use redis" in text:
        return Intent.GET_DEPENDENTS, {"node": "redis-main"}

    # Blast radius
    if "what breaks" in text or "blast radius" in text:
        node = extract_entity(text)
        return Intent.BLAST_RADIUS, {"node": node} if node else (Intent.UNKNOWN, {})

    # Path ✅ FIXED
    # Path
    if "how does" in text and "connect to" in text:
      entities = re.findall(
            r"(api-gateway|[a-z0-9\-]+-(?:service|db))",
            text
        )
    #   print("🧪 PATH ENTITIES:", entities)
      if len(entities) >= 2:
        return Intent.SHORTEST_PATH, {
            "from": entities[0],
            "to": entities[1]
        }
    # Exploration
    if "list all services" in text:
        return Intent.LIST_SERVICES, {}

    if "show all databases" in text:
        return Intent.LIST_DATABASES, {}

    if "what teams are there" in text:
        return Intent.LIST_TEAMS, {}

    return Intent.UNKNOWN, {}
