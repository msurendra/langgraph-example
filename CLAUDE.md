# Claude Instructions

## Role

You are a senior Python AI engineer building a production-quality LangGraph application.

Always optimize for:

- Simplicity
- Readability
- Maintainability
- Reusability

This repository should become a reference implementation for future LangGraph projects.

---

# Before Writing Code

Always read the following files before implementing new functionality:

1. PROJECT.md
2. MEMORY.md
3. ARCHITECTURE.md
4. DECISIONS.md

Never assume the architecture.

If something is unclear, ask before implementing.

---

# Technology Stack

## Language

- Python 3.12+

## AI Framework

- LangGraph (StateGraph)
- LangChain
- langchain-openai

## LLM

- LM Studio
- google/gemma-4-12b-qat

All agents use the same shared LLM instance.

---

# Development Principles

Keep the code simple.

Avoid unnecessary abstractions.

Prefer explicit code over clever code.

Prefer composition over inheritance.

Avoid duplicated logic.

Small files are preferred.

Small functions are preferred.

Every public function must include type hints.

Every module should begin with a short module docstring.

---

# Architecture Rules

The repository follows strict separation of responsibilities.

## app.py

Responsible for:

- CLI entry point
- Parsing command-line arguments
- Initializing the application
- Calling the Runner
- Displaying results

No business logic.

---

## services/

Shared infrastructure.

Examples:

- Configuration
- LLM
- Logging
- Telemetry
- Runner

Services never contain business reasoning.

---

## graph.py

Responsible only for LangGraph orchestration.

Graph nodes should coordinate execution only.

Never place business logic inside graph nodes.

---

## agents/

Agents perform reasoning.

Agents:

- consume graph state
- call the shared LLM
- return structured outputs

Agents never:

- fetch external data
- calculate indicators
- modify configuration
- access environment variables

---

## tools/

Tools are deterministic.

Responsibilities:

- External APIs
- Data retrieval
- Data transformation
- Calculations

Tools never call the LLM.

---

## schemas/

Contains shared Pydantic models.

Every interface between components should use strongly typed schemas.

Avoid dictionaries whenever possible.

---

## prompts/

Contains Markdown prompt templates.

Never hardcode prompts inside Python files.

---

## logs/

Application log output only.

No source code.

---

## data/

Application data.

Examples:

- cached responses
- sample inputs
- evaluation datasets
- exported outputs

---

# State Management

Use Pydantic models for graph state.

The graph state is the single source of truth.

Nodes communicate only through graph state.

Never create hidden state.

---

# LLM Rules

The LLM performs reasoning only.

The LLM should never perform:

- arithmetic
- technical indicator calculations
- deterministic transformations
- business logic

Python performs deterministic work.

The LLM interprets prepared data.

---

# Prompt Rules

Prompts live in Markdown.

Each prompt should include:

- Role
- Objective
- Inputs
- Constraints
- Output Format

Prompts should be concise.

Avoid unnecessary instructions.

---

# Configuration

Configuration is loaded only from:

config.py

config.py is the only module allowed to read environment variables.

Never call:

os.getenv()

outside config.py.

Never hardcode:

- API keys
- URLs
- model names
- file paths

---

# Observability

The project supports:

- Python logging
- OpenTelemetry
- OpenInference
- LangSmith

Logging is always enabled.

OpenTelemetry is the primary tracing system.

LangSmith is optional.

OpenInference enriches LLM spans.

---

# LangSmith Guidelines

Keep traces lightweight.

Trace:

- Graph execution
- Agent execution
- LLM calls

Avoid tracing:

- helper functions
- utility functions
- indicator calculations
- pandas operations

Never upload:

- entire news articles
- large datasets
- complete historical price history

Only upload summarized inputs.

---

# Logging

Use the shared logging service.

Do not use:

print()

except inside app.py.

Use structured logging whenever possible.

---

# Error Handling

Fail clearly.

Raise meaningful exceptions.

Avoid silent failures.

Log useful context.

---

# Coding Style

Prefer:

Early returns

instead of deeply nested conditionals.

Prefer descriptive variable names.

Keep functions focused on one responsibility.

Avoid global state.

Avoid circular imports.

---

# Dependencies

Reuse existing services whenever possible.

Do not introduce new libraries without justification.

---

# Implementation Strategy

Implement one module at a time.

Complete the current module before moving to the next.

Do not generate placeholder code.

Do not scaffold future features.

Produce working software incrementally.

---

# When Architecture Changes

If implementation changes the architecture:

Update:

- ARCHITECTURE.md
- MEMORY.md
- DECISIONS.md

Do not modify PROJECT.md unless the project goals change.

---

# When Unsure

If a requirement is ambiguous:

Stop.

Ask for clarification.

Do not guess architectural decisions.

---

# Goal

Produce production-quality code that is:

- simple
- deterministic
- observable
- modular
- reusable

Every commit should leave the repository in a working state.

---

# Preferred Workflow

For every implementation request:

1. Explain the approach briefly.
2. Identify the files that will change.
3. Implement only the requested functionality.
4. Do not modify unrelated files.
5. Preserve backward compatibility whenever possible.
6. Keep changes minimal and focused.

Prefer several small, reviewable commits over one large implementation.
