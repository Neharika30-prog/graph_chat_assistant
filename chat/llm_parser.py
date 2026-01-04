import subprocess
import json
from chat.intents import Intent

def call_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def llm_parse(text: str):
    print("🤖 LLM PARSER USED")

    prompt = f"""
You are an intent classifier for a graph query system.

Return JSON ONLY in this format:
{{
  "intent": "GET_OWNER | GET_DEPENDENCIES | GET_DEPENDENTS | BLAST_RADIUS | SHORTEST_PATH | UNKNOWN",
  "node": null,
  "from": null,
  "to": null
}}

User query:
{text}
"""

    try:
        response = call_llm(prompt)
        data = json.loads(response)

        intent = Intent[data["intent"]]
        params = {k: v for k, v in data.items() if k != "intent" and v}

        return intent, params
    except Exception as e:
        print("⚠️ LLM parsing failed:", e)
        return Intent.UNKNOWN, {}
