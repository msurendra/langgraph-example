# Setup

## Prerequisites

- Python 3.10+
- LM Studio running locally with `google/gemma-4-12b-qat` loaded

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Create `.env.local` in the project root:

```
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=google/gemma-4-12b-qat

LANGSMITH_TRACING=false

LOG_LEVEL=INFO

OTEL_SERVICE_NAME=langgraph-example
```

## Run

Basic:
```bash
python app.py AAPL
```

With streaming (see node-by-node progress):
```bash
python app.py AAPL --stream
```

With debug logging (LangGraph internals):
```bash
python app.py AAPL --debug
```

Visualize the graph (prints Mermaid diagram):
```bash
python app.py AAPL --visualize
```

Paste the Mermaid output at https://mermaid.live to see it rendered.

## Monitoring

### Phoenix UI (recommended)

```bash
pip install arize-phoenix
python -m phoenix.server.main serve
```

Open http://localhost:6006, then run the app in another terminal. All LLM traces (prompts, responses, latency, tokens) appear in the dashboard. Traces persist across runs.

### Local trace logs

Traces also write to `logs/traces.jsonl` automatically. View them with:

```bash
cat logs/traces.jsonl | python -m json.tool
```

### Application logs

```bash
cat logs/app.log
```
