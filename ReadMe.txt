Graph Chat Assistant

An end-to-end system that parses infrastructure configuration files (Docker Compose, Teams, Kubernetes), builds a unified dependency graph in Neo4j, and exposes a natural language chat interface to query ownership, dependencies, blast radius, and paths between services.

1. Setup & Usage
Prerequisites

Docker & Docker Compose

Node.js (only if running frontend locally)

(Optional) Ollama installed for local LLM inference

How to Start

Single-command startup (as required):docker-compose up

This command:

1.Starts Neo4j

2.Runs ingestion connectors

3.Populates the graph

4.Starts FastAPI backend

5.Starts React + Vite chat UI

Accessing the System

Chat UI: http://localhost:3000

Backend API: http://localhost:8000

Neo4j Browser: http://localhost:7474

Username: neo4j

Password: password

How to Use the Chat Interface

Type natural language questions such as:

Who owns payment-service?

What breaks if redis-main goes down?

How does api-gateway connect to payments-db?

List all services

What teams are there?

The system translates these queries into graph traversals and returns structured answers.

Environment Variables

The system uses environment variables with safe defaults:
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

No external API keys are required.
LLM inference is handled locally using Ollama

2. Architecture Overview
High-Level Data Flow

Config Files
(docker-compose.yml, teams.yaml, k8s.yaml)
        ↓
Connectors (Docker / Teams / K8s)
        ↓
Unified Graph Format (nodes + edges)
        ↓
Neo4j Graph Storage
        ↓
Query Engine (ownership, deps, blast radius, paths)
        ↓
FastAPI Backend
        ↓
React + Vite Chat UI

Key Components

Connectors

Parse raw configuration files

Normalize them into graph nodes & edges

Graph Storage (Neo4j)

Persists services, databases, teams, and relationships

Survives container restarts

Query Engine

Executes graph traversals (upstream, downstream, blast radius, shortest path)

Chat Interface

React + Vite frontend

Uses an LLM-based parser (Ollama) to map natural language → graph queries

3. Design Questions
1. Connector Pluggability

New connectors can be added by implementing a parser that outputs nodes and edges in the same normalized format. The ingestion pipeline is connector-agnostic, so adding Terraform or other infra formats only requires a new connector module and minimal wiring.

Key Components

Connectors

Parse raw configuration files

Normalize them into graph nodes & edges

Graph Storage (Neo4j)

Persists services, databases, teams, and relationships

Survives container restarts

Query Engine

Executes graph traversals (upstream, downstream, blast radius, shortest path)

Chat Interface

React + Vite frontend

Uses an LLM-based parser (Ollama) to map natural language → graph queries

3. Design Questions

1. Connector Pluggability

New connectors can be added by implementing a parser that outputs nodes and edges in the same normalized format. The ingestion pipeline is connector-agnostic, so adding Terraform or other infra formats only requires a new connector module and minimal wiring.

2. Graph Updates

The graph uses upsert semantics (MERGE in Neo4j). When configuration files change, re-running ingestion updates existing nodes and relationships instead of duplicating them, keeping the graph consistent with source configs.

3. Cycle Handling

Traversal queries use bounded depth and Neo4j’s path semantics to avoid infinite loops. Cycles are naturally handled by the graph database without repeated visits.

4. Query Mapping (Natural Language → Graph)

User queries are classified into intent categories (ownership, dependency, blast radius, path). An LLM (Ollama) extracts entities and intent, which are mapped to predefined graph queries instead of free-form Cypher, preventing hallucination.

5. Failure Handling

If a query cannot be mapped confidently, the system returns a safe fallback message instead of guessing. Only supported query patterns are executed, ensuring correctness over creativity.
 6. Scale Considerations

At ~10K nodes, traversal depth and query performance would degrade first. Improvements would include indexed properties, query caching, async ingestion, and pre-computed dependency summaries.

7. Graph DB Choice

Neo4j was chosen for its native graph traversal support, expressive Cypher language, and ease of modeling dependencies compared to relational databases.

4. Tradeoffs & Limitations

Kubernetes connector is optional and limited

No incremental file watcher (manual re-ingestion)

No authentication or multi-tenant support

LLM prompt logic is intentionally constrained to avoid hallucinations

5. AI Usage
Where AI Helped Most

Designing query intent classification

Translating natural language into structured graph queries

Improving UX of the chat interface

Where AI Was Corrected

Docker + Neo4j networking assumptions

Python import paths inside containers

Dependency ordering during startup

Key Learning

AI accelerates system design but still requires strong debugging and architectural judgment, especially in distributed systems.

6. Demo Video (3–5 Minutes)

The demo covers:

docker-compose up startup

Connectors parsing config files

Graph population in Neo4j

5+ natural language queries

At least one blast radius or path query

One design decision explained

Link-

7. Repository Structure

.
├── docker-compose.yml
├── api/
├── ingest/
├── connectors/
├── graph/
├── chat/
├── frontend/
├── infra/
└── README.md


