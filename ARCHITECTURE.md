# Architecture

## Overview

This application demonstrates a production-quality multi-agent workflow built using LangGraph.

The goal is to separate deterministic software from LLM reasoning while maintaining a clean, modular, and observable architecture.

The application accepts a stock ticker, gathers market data, performs multiple analyses in parallel, and produces a structured recommendation.

---

# High-Level Flow

```text
                  python app.py <TICKER>
                          │
                          ▼
                     app.py (CLI)
                          │
                          ▼
                services.runner.Runner
                          │
                          ▼
               LangGraph (StateGraph)
                          │
                          ▼
                 Collect Data Node
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
 Technical Agent   Fundamental Agent   News Agent
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  Decision Agent
                          │
                          ▼
            BUY / HOLD / SELL Recommendation
```

---

# Layered Architecture

```text
                Presentation Layer
                      (CLI)
                         │
                         ▼
                Application Layer
                     (Runner)
                         │
                         ▼
                 Orchestration Layer
                    (LangGraph)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Technical        Fundamental         News
      Agent            Agent           Agent
        └────────────────┼────────────────┘
                         ▼
                 Decision Agent
                         │
                         ▼
                 Shared Services
                         │
      ┌──────────┬───────┼───────┬──────────┐
      ▼          ▼       ▼       ▼          ▼
    LLM       Tools   Logging  Telemetry  Memory
```

---

# Responsibilities

## app.py

Application entry point.

Responsible for:

- Parse CLI arguments
- Initialize application
- Invoke Runner
- Display results

No business logic.

---

## Runner

Coordinates one complete execution.

Responsible for:

- Build initial graph state
- Invoke LangGraph
- Return final recommendation

The Runner should be reusable by:

- CLI
- REST API
- Streamlit
- Future integrations

---

## Graph

Defines the LangGraph workflow.

Responsible for:

- Node orchestration
- State transitions
- Parallel execution
- Error propagation

The graph never contains business logic.

---

## Agents

Agents perform reasoning.

Responsibilities:

- Consume graph state
- Analyze data
- Generate structured outputs

Agents never:

- Call external APIs
- Calculate indicators
- Access configuration
- Read environment variables

---

## Tools

Tools perform deterministic work.

Responsibilities:

- Fetch market data
- Fetch news
- Perform calculations
- Normalize data

Tools never call the LLM.

---

## Services

Shared infrastructure.

Examples:

- Configuration
- LLM
- Logging
- Telemetry
- Runner

Services contain no business reasoning.

---

## Memory

Long-term memory using mem0.

Responsibilities:

- Store past recommendations per ticker
- Recall prior analyses for context
- Provide trend awareness to the decision agent

Memory is persisted locally using ChromaDB with HuggingFace embeddings.

The decision agent receives past analyses as additional context when available.

---

## Schemas

Shared contracts.

All communication between components uses strongly typed Pydantic models.

Avoid dictionaries whenever possible.

---

## Prompts

Prompt templates stored as Markdown.

Prompts are version-controlled independently of Python code.

---

# Execution Flow

## Step 1

User executes

```bash
python app.py NVDA
```

---

## Step 2

Runner recalls past analyses from memory and creates the initial graph state.

---

## Step 3

Collect Data node retrieves:

- Market data
- Historical data
- Company fundamentals
- Recent news

Data is fetched exactly once.

---

## Step 4

Analysis agents execute in parallel.

- Technical
- Fundamental
- News

Each agent receives the same shared graph state.

---

## Step 5

Decision Agent combines the outputs along with past analyses from memory.

Produces:

- Recommendation
- Confidence
- Supporting reasons

---

## Step 6

Runner stores the recommendation in memory and returns the result.

CLI renders the output.

---

# Shared State

The graph state is the single source of truth.

Example contents include:

- ticker
- market information
- calculated metrics
- company fundamentals
- news summary
- past analyses (from memory)
- technical analysis
- fundamental analysis
- news analysis
- final recommendation

Nodes communicate only through graph state.

---

# Parallel Execution

The following nodes execute concurrently.

```text
          Collect Data
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
Technical   Fundamental   News
     └──────────┼──────────┘
                ▼
          Decision Agent
```

Parallel execution reduces overall latency while keeping agents independent.

---

# LLM Architecture

A single shared LLM instance is used.

```text
                 LM Studio
                      │
                      ▼
               Shared ChatOpenAI
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Technical      Fundamental        News
      Agent          Agent         Agent
                      │
                      ▼
               Decision Agent
```

No agent creates its own LLM instance.

---

# Configuration

Configuration is centralized.

Only `config.py` reads environment variables.

Every component imports configuration from `config.py`.

---

# Observability

Observability is built into every execution.

## Logging

Structured application logs.

Used for:

- execution progress
- warnings
- errors

---

## OpenTelemetry

Primary tracing system.

Every graph node creates a trace span.

---

## OpenInference

Adds AI-specific metadata to LLM spans.

Examples:

- prompts
- model
- latency
- token usage

---

## Phoenix

Primary observability UI.

Displays:

- LLM traces
- prompts and responses
- latency and token usage

Runs locally at http://localhost:6006.

---

## LangSmith

Optional.

Used for debugging.

Only traces:

- graph execution
- LLM calls

Avoid tracing helper functions.

Avoid uploading large datasets.

---

# Error Handling

Errors should propagate through the graph.

Every failure should include:

- meaningful message
- structured logs
- trace information

Avoid silent failures.

---

# Design Principles

- Fetch external data once.
- Share state through LangGraph.
- Python performs deterministic work.
- LLM performs reasoning.
- Keep components independent.
- Keep interfaces strongly typed.
- Keep orchestration separate from business logic.
- Build with observability from day one.
- Optimize for readability over cleverness.
- Prefer reusable components over application-specific code.

---

# Future Extensibility

The architecture should support adding new agents without changing existing ones.

Examples:

- Risk Agent
- Portfolio Agent
- Macro Agent
- Earnings Agent
- Valuation Agent

New agents should consume shared graph state and return structured outputs without affecting the existing workflow.
