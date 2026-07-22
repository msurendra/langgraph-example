# LangGraph Example

Production-quality multi-agent stock analyzer built with LangGraph.

Demonstrates clean architecture, parallel agent execution, structured LLM outputs, long-term memory, and local observability.

## Stack

- **LLM**: LM Studio + Gemma 4 (local)
- **Orchestration**: LangGraph (StateGraph)
- **Memory**: mem0 + ChromaDB
- **Observability**: OpenTelemetry + OpenInference + Phoenix
- **Data**: Yahoo Finance, DuckDuckGo News

## How It Works

```
CLI → Runner → LangGraph
                  │
            Collect Data
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  Technical   Fundamental   News
    Agent       Agent      Agent
       └──────────┼──────────┘
                  ▼
           Decision Agent → BUY / HOLD / SELL
```

- Data is fetched once and shared via graph state
- Three analysis agents run in parallel
- Decision agent synthesizes all analyses plus past memory
- Each run is stored in mem0 for future context

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env.local`:

```
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=google/gemma-4-12b-qat
LANGSMITH_TRACING=false
LOG_LEVEL=INFO
OTEL_SERVICE_NAME=langgraph-example
```

Start LM Studio with the model loaded, then:

```bash
python app.py AAPL
```

## CLI Options

```bash
python app.py AAPL              # basic analysis
python app.py AAPL --stream     # watch node-by-node progress
python app.py AAPL --debug      # LangGraph internal logging
python app.py AAPL --visualize  # print graph diagram (Mermaid)
python app.py AAPL --history    # view past analyses from memory
```

## Monitoring

### Phoenix (recommended)

```bash
python -m phoenix.server.main serve
```

Open http://localhost:6006 to view LLM traces, prompts, responses, latency, and token usage across all runs.

### Local logs

```bash
cat logs/traces.jsonl | python -m json.tool   # OpenTelemetry traces
cat logs/app.log                               # application logs
```

## Memory (mem0 + ChromaDB)

Past analyses are stored per ticker and recalled on future runs. Data persists in `data/mem0/`.

**View past analyses for a ticker:**

```bash
python app.py AAPL --history
```

**Search across all tickers:**

```python
python -c "
from services.memory import search_analyses
for m in search_analyses('bullish momentum'):
    print(m)
"
```

**Inspect raw ChromaDB storage:**

```python
python -c "
import chromadb
client = chromadb.PersistentClient(path='data/mem0')
for col in client.list_collections():
    print(f'Collection: {col.name}')
    data = col.get(include=['documents', 'metadatas', 'embeddings'])
    for i, doc in enumerate(data['documents']):
        print(f'\n--- Record {i} ---')
        print(f'Document: {doc}')
        print(f'Metadata: {data[\"metadatas\"][i]}')
        print(f'Embedding dims: {len(data[\"embeddings\"][i]) if data[\"embeddings\"] else \"N/A\"}')
"
```

**Browse raw files on disk:**

```bash
find data/mem0 -type f
```

## Project Structure

```
app.py              CLI entry point
config.py           Centralized configuration
graph.py            LangGraph workflow

agents/             LLM reasoning (technical, fundamental, news, decision)
tools/              Deterministic work (market data, news, indicators)
services/           Shared infrastructure (LLM, logging, memory, telemetry)
schemas/            Pydantic models
prompts/            Markdown prompt templates
logs/               Traces and application logs
data/               Memory storage and cached data
```

See [SETUP.md](SETUP.md) for detailed setup instructions, [ARCHITECTURE.md](ARCHITECTURE.md) for design details.
