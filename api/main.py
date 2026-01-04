from unittest import result
from fastapi import FastAPI
from pydantic import BaseModel

from graph.storage import GraphStorage
from graph.query import GraphQueryEngine
from chat.dispatcher import QueryDispatcher
from chat.nl_parser import parse_query
from chat.llm_parser import llm_parse
from chat.formatter import format_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Graph Chat Assistant",
    description="Natural language interface over infrastructure knowledge graph",
    version="1.0"
)

# ---- Initialize graph system once ----
store = GraphStorage()
query_engine = GraphQueryEngine(store)
dispatcher = QueryDispatcher(query_engine)

# Simple in-memory session (OK for assignment)
SESSION = {
    "last_node": None,
    "last_intent": None
}

# ---- Request / Response models ----
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    path: list[str] | None = None


# ---- Chat endpoint ----
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    text = req.message

    intent, params = parse_query(
        text
    )

    # LLM fallback
    if intent.name == "UNKNOWN":
        intent, params = llm_parse(text)

        if intent.name == "UNKNOWN":
            return ChatResponse(
                reply="🤔 I’m not sure what you mean. Try asking about services, dependencies, or blast radius."
            )

    result = dispatcher.dispatch(intent, params)

    if intent.name == "SHORTEST_PATH":
        return ChatResponse(
            reply=" → ".join(result),
            path=result          
        )

    if "node" in params:
        SESSION["last_node"] = params["node"]
        SESSION["last_intent"] = intent

    if intent.name == "SHORTEST_PATH" and isinstance(result, list):
      return ChatResponse(
        reply=" → ".join(result),
        path=result
      )

     # ---- Default response ----
    reply = format_response(intent, result)
    return ChatResponse(reply=reply)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for assignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

