from chat.intents import Intent

def format_response(intent, result):
    if intent == Intent.GET_OWNER:
        return ", ".join(result) if result else "No owner found."

    if intent == Intent.GET_DEPENDENCIES:
        return ", ".join(result) if result else "No dependencies found."

    if intent == Intent.GET_DEPENDENTS:
        return ", ".join(result) if result else "No dependents found."

    if intent == Intent.BLAST_RADIUS:
        return f"Affected nodes: {result}"

    if intent == Intent.SHORTEST_PATH:
        return " → ".join(result) if result else "No path found."

    if intent == Intent.LIST_SERVICES:
        return ", ".join(result)

    if intent == Intent.LIST_DATABASES:
        return ", ".join(result)

    if intent == Intent.LIST_TEAMS:
        return ", ".join(result)

    return "I couldn’t find an answer."
