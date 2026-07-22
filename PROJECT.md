# LangGraph Example

## Overview

This repository demonstrates how to build a production-quality AI application using LangGraph.

The goal is to provide a clean, reusable reference implementation that follows modern software engineering practices while remaining simple enough to understand and extend.

Although the initial use case is stock analysis, the architecture is intentionally generic so it can be reused for other agentic workflows.

---

# Objectives

This project focuses on demonstrating:

- Clean architecture
- Modular AI agents
- Deterministic software design
- Structured LLM outputs
- Observable AI systems
- Production-ready project organization

---

# Current Use Case

Analyze a stock ticker using multiple AI agents.

Each agent evaluates a different aspect of the company before a final decision is produced.

Example

```bash
python app.py AAPL
```

Expected output:

- BUY
- HOLD
- SELL

with confidence and supporting reasoning.

---

# Technology Stack

## Language

- Python 3.12+

## AI Framework

- LangGraph (StateGraph)
- LangChain
- langchain-openai

## Local Model

- LM Studio
- google/gemma-4-12b-qat

## Data Sources

- Yahoo Finance
- DuckDuckGo Search

## Data Processing

- Pandas

## Data Validation

- Pydantic v2

---

# Engineering Principles

## Separation of Responsibilities

Every layer has one responsibility.

- CLI handles user interaction.
- Runner coordinates execution.
- Graph orchestrates workflow.
- Agents perform reasoning.
- Tools perform deterministic work.
- Services provide shared infrastructure.

---

## Deterministic First

Python performs deterministic work.

Examples:

- calculations
- transformations
- validation
- API communication

The LLM performs reasoning only.

---

## Shared State

All agents communicate through LangGraph state.

No hidden state.

No direct communication between agents.

---

## Strong Contracts

Communication between components uses strongly typed Pydantic models.

Avoid loosely structured dictionaries.

---

## Observability by Default

Every execution should be observable.

The application supports:

- Structured Logging
- OpenTelemetry
- OpenInference
- LangSmith

Observability should require minimal changes to application code.

---

## Reusable Components

Every component should be reusable.

Examples:

- Runner
- LLM Service
- Logging
- Tools
- Agents

The stock analysis workflow should not tightly couple the architecture to the finance domain.

---

# Repository Structure

```
app.py

graph.py

config.py

agents/

tools/

services/

schemas/

prompts/

logs/

data/
```

Each directory has a single responsibility.

---

# Configuration

Application configuration is loaded from:

`.env.local`

Secrets are never committed to source control.

All configuration is accessed through:

`config.py`

---

# Success Criteria

The project is considered successful if it demonstrates:

- Clear separation of concerns
- Parallel agent execution
- Strong typing
- Structured outputs
- Local LLM execution
- Easy debugging
- Production-quality organization

---

# Future Direction

This repository should become a reusable template for future LangGraph applications.

Future use cases may include:

- Multi-agent workflows
- RAG applications
- Planning agents
- Research assistants
- Enterprise AI systems

without requiring architectural changes.
---
# Non-Goals

This repository is not intended to demonstrate:

- complex financial strategies
- high-frequency trading
- portfolio optimization
- backtesting
- advanced quantitative analysis

The focus is AI engineering, software architecture, and LangGraph best practices.
