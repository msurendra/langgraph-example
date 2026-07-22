# Project Memory

## Project Status

Status: Implemented

Core application is fully implemented and functional.

---

# Current Goal

Build a production-quality multi-agent LangGraph application that demonstrates modern AI engineering practices.

The current use case is stock analysis.

The architecture is intentionally generic so it can be reused for future projects.

---

# Current Technology Stack

Language

- Python 3.12+

Frameworks

- LangGraph (StateGraph)
- LangChain
- langchain-openai

Model

- google/gemma-4-12b-qat

Model Host

- LM Studio

Validation

- Pydantic v2

Memory

- mem0
- ChromaDB
- HuggingFace embeddings (all-MiniLM-L6-v2)

Observability

- Phoenix (Arize)
- OpenTelemetry
- OpenInference

---

# Current Execution Flow

```text
User

↓

app.py

↓

Runner

↓

LangGraph

↓

Prepare Context

↓

Parallel Analysis

- Technical Agent
- Fundamental Agent
- News Agent

↓

Decision Agent

↓

Recommendation
```

---

# Current Components

Application

- app.py
- config.py
- graph.py

Agents

- Technical Agent
- Fundamental Agent
- News Agent
- Decision Agent

Services

- Runner
- LLM
- Logging
- Telemetry
- Memory
- Prompt Loader
- JSON Parsing

Tools

- Market Data (Yahoo Finance)
- News (DuckDuckGo)
- Technical Indicators (ta library)

---

# Current Design Decisions

A single shared LLM instance is used.

Graph state is the single source of truth.

External data is fetched once.

Agents consume shared graph state.

Agents execute in parallel.

Agents return structured outputs.

Python performs deterministic work.

LLMs perform reasoning only.

---

# Current Observability

Structured logging (structlog)

OpenTelemetry traces exported to local file and Phoenix

OpenInference LangChain instrumentation

Phoenix UI at http://localhost:6006

Optional LangSmith (disabled by default)

---

# Current Configuration

Configuration is loaded from:

`.env.local`

Configuration is accessed only through:

`config.py`

No module except config.py should read environment variables.

---

# Current Prompt Strategy

Prompts are stored as Markdown.

Each agent owns one prompt.

Prompts are independent from Python code.

---

# Current State Model

The graph state contains:

- User input (ticker)
- Market data
- Company information
- Fundamentals
- Technical indicators
- News items
- Past analyses (from mem0)
- Agent outputs (technical, fundamental, news)
- Final recommendation

State is represented using Pydantic models.

---

# Current Principles

Keep components loosely coupled.

Keep files small.

Keep functions focused.

Keep interfaces strongly typed.

Prefer deterministic software over prompt complexity.

---

# Notes for Future Development

Do not introduce unnecessary abstractions.

Do not duplicate logic across agents.

Prefer reusable services.

Prefer incremental implementation.

Implement one module at a time.

Keep the repository in a working state after every change.
