def format_response(intent, result):
    if not result:
        return "I couldn't find an answer for that."

    if isinstance(result, dict):
        return f"Affected nodes: {result['affected_nodes']}"

    if isinstance(result, list):
        return ", ".join(result)

    return str(result)
