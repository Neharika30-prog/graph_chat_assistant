from graph.storage import GraphStorage
from graph.query import GraphQueryEngine

store = GraphStorage()
query = GraphQueryEngine(store)

print("GET NODE:")
print(query.get_node("payment-service"))

print("\nDOWNSTREAM (ALL EDGES):")
print(query.downstream("order-service"))

print("\nDOWNSTREAM (ONLY CALLS):")
print(query.downstream("order-service", edge_types=["CALLS"]))

print("\nUPSTREAM:")
print(query.upstream("orders-db"))

print("\nBLAST RADIUS:")
print(query.blast_radius("order-service"))

print("\nSHORTEST PATH:")
print(query.path("api-gateway", "payments-db"))

print("\nOWNER:")
print(query.get_owner("payment-service"))

store.close()

