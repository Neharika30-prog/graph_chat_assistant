from graph.storage import GraphStorage
from graph.query import GraphQueryEngine
from chat.nl_parser import parse_query
from chat.dispatcher import QueryDispatcher
from chat.response import format_response

def main():
    
    store = GraphStorage()
    query_engine = GraphQueryEngine(store)
    dispatcher = QueryDispatcher(query_engine)

    last_node = None
    last_intent = None

    print("🔹 Graph Chat Assistant (type 'exit' to quit)")

    while True:
        user_input = input("\n> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        intent, params = parse_query(user_input)

        if intent.name == "UNKNOWN":
           from chat.llm_parser import llm_parse
           intent, params = llm_parse(user_input)

           if intent.name == "UNKNOWN":
              print("🤔 I’m not sure what you mean.")
              print("Try asking things like:")
              print(" • Who owns payment-service?")
              print(" • What does order-service depend on?")
              print(" • What breaks if redis-main goes down?")
              print(" • How does api-gateway connect to payments-db?")
              continue


        result = dispatcher.dispatch(intent, params)
        if "node" in params:
           last_node = params["node"]
           last_intent = intent

        print("➡️", format_response(intent, result))

    store.close()

if __name__ == "__main__":
    main()
