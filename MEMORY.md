# Project Memory

## Project Status

Status: Initial Development

The repository structure has been established.

Architecture documentation is complete.

Implementation has not yet started.

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

Tools

- Market Data
- News
- Data Processing

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

Logging

OpenTelemetry

OpenInference

Optional LangSmith

LangSmith should trace only graph execution and LLM calls.

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

- User input
- Market information
- Company information
- News summary
- Agent outputs
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
