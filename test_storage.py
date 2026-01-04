from graph.storage import GraphStorage

store = GraphStorage()

store.upsert_node("Service", "payment-service")
store.upsert_node("Team", "payments-team")

store.upsert_edge("payments-team", "OWNS", "payment-service")

print(store.get_node("payment-service"))
print(store.get_nodes_by_type("Service"))

store.close()
