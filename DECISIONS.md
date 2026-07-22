# Architecture Decision Records (ADR)

This document records significant architectural decisions made during the project.

Each decision includes:

- Decision
- Reason
- Consequences

Only record decisions that affect the overall architecture.

---

# ADR-001

## Decision

Use LangGraph StateGraph.

## Reason

StateGraph provides explicit workflow orchestration, shared state management, parallel execution, and future extensibility.

## Consequences

- Clear execution flow
- Easy visualization
- Predictable state transitions
- Easier debugging

---

# ADR-002

## Decision

Use a single shared LLM instance.

## Reason

Creating one shared ChatOpenAI instance reduces resource usage and provides consistent behavior across all agents.

## Consequences

- Lower memory usage
- Consistent configuration
- Easier model replacement

---

# ADR-003

## Decision

Serve the model locally through LM Studio.

## Model

google/gemma-4-12b-qat

## Reason

Local inference provides predictable behavior, lower cost, offline development, and complete control over the execution environment.

## Consequences

- No dependency on hosted APIs
- Easy model experimentation
- Faster local iteration

---

# ADR-004

## Decision

Use Pydantic for all schemas.

## Reason

Strong typing improves validation, serialization, IDE support, and maintainability.

## Consequences

- Consistent interfaces
- Better error messages
- Safer refactoring

---

# ADR-005

## Decision

All agents share a common graph state.

## Reason

Graph state becomes the single source of truth.

Agents remain independent while communicating through structured state.

## Consequences

- Loose coupling
- Easier testing
- Easier replay
- Better observability

---

# ADR-006

## Decision

External data is fetched once.

## Reason

Avoid duplicate API calls and ensure all agents analyze identical data.

## Consequences

- Faster execution
- Consistent analysis
- Reduced external API usage

---

# ADR-007

## Decision

Analysis agents execute in parallel.

## Reason

Technical, Fundamental, and News analysis are independent tasks.

## Consequences

- Lower latency
- Better scalability
- Independent agents

---

# ADR-008

## Decision

Python performs deterministic work.

LLMs perform reasoning.

## Reason

Deterministic logic should remain predictable and testable.

LLMs should focus on interpretation rather than calculations.

## Consequences

Python is responsible for:

- calculations
- transformations
- validation

LLMs are responsible for:

- reasoning
- summarization
- recommendations

---

# ADR-009

## Decision

Prompts are stored as Markdown.

## Reason

Separating prompts from Python simplifies maintenance and version control.

## Consequences

- Easier prompt iteration
- Cleaner Python code
- Better prompt reuse

---

# ADR-010

## Decision

Configuration is centralized.

Only config.py may access environment variables.

## Reason

Centralizing configuration reduces duplication and prevents configuration drift.

## Consequences

- Easier testing
- Cleaner code
- Simpler deployment

---

# ADR-011

## Decision

Use OpenTelemetry as the primary observability standard.

## Reason

OpenTelemetry is vendor-neutral and integrates with multiple observability platforms.

## Consequences

The application can export traces to different backends without changing business logic.

---

# ADR-012

## Decision

Use OpenInference for LLM instrumentation.

## Reason

OpenInference enriches traces with AI-specific metadata while remaining compatible with OpenTelemetry.

## Consequences

LLM interactions include:

- prompts
- responses
- latency
- model information
- token usage

without changing application code.

---

# ADR-013

## Decision

Use LangSmith only for debugging.

## Reason

The free tier is limited.

Only high-value execution information should be uploaded.

## Consequences

Trace only:

- Graph execution
- Agent execution
- LLM calls

Avoid tracing:

- helper functions
- utilities
- calculations
- pandas operations

---

# ADR-014

## Decision

Keep LangSmith traces lightweight.

## Reason

Large payloads increase latency and consume free-tier quotas.

## Consequences

Do not upload:

- full historical price data
- complete news articles
- large API responses

Only upload summarized context.

---

# ADR-015

## Decision

Application follows a layered architecture.

## Layers

Presentation

↓

Application

↓

Orchestration

↓

Agents

↓

Tools

↓

Infrastructure

## Reason

Each layer has one responsibility.

## Consequences

Improved maintainability and easier future extension.

---

# ADR-016

## Decision

Application execution flows through Runner.

Execution path:

CLI

↓

Runner

↓

LangGraph

↓

Agents

## Reason

The Runner becomes the reusable application entry point.

Future interfaces such as REST APIs or Streamlit can reuse the same execution flow.

## Consequences

Business logic remains independent of the presentation layer.

---

# ADR-017

## Decision

Every agent returns structured output.

## Reason

Structured outputs improve reliability, validation, and downstream processing.

## Consequences

Agent communication uses Pydantic models rather than free-form text.

---

# ADR-018

## Decision

The architecture should remain domain-independent.

## Reason

Although the first implementation analyzes stocks, the architecture should support future AI workflows without significant redesign.

## Consequences

Business-specific logic stays within tools, prompts, and agents.

Core infrastructure remains reusable.
---
# ADR-019

## Decision

Keep deterministic code outside the LLM.

## Rule

If a problem can be solved reliably with Python, solve it with Python.

Use the LLM only where semantic reasoning or natural language understanding adds value.

## Reason

This keeps the system predictable, testable, easier to debug, and less expensive to run.

## Consequences

Before introducing an LLM into any new feature, first determine whether the task can be implemented deterministically.

---

# ADR-020

## Decision

Use mem0 for long-term memory.

## Reason

mem0 provides simple memory management with semantic search, local persistence via ChromaDB, and lightweight integration. It runs entirely locally, consistent with the project's local-first approach.

## Consequences

- Past analyses are stored per ticker
- Decision agent receives historical context
- Memory persists across runs in `data/mem0/`
- HuggingFace embeddings (all-MiniLM-L6-v2) are used for vector search
- No external API dependency

---

# ADR-021

## Decision

Use Phoenix (Arize) as the primary observability UI.

## Reason

Phoenix is open-source, runs locally, and natively supports OpenInference traces. It provides LLM-specific insights (prompts, responses, latency, token usage) that generic trace viewers lack.

## Consequences

- Traces are exported to Phoenix via OTLP
- Local file export remains as fallback
- LangSmith is optional and disabled by default
