# Future Roadmap

Features to evolve this into a production-grade agentic harness.

---

## Core

### Interactive / Conversational Mode

Multi-turn dialogue instead of one-shot execution.

| Framework | How |
|-----------|-----|
| LangGraph | `MemorySaver` / `SqliteSaver` persists conversation state across turns |
| Streamlit | `st.chat_input()` + `st.chat_message()` for quick chat UI |
| Chainlit | Full-featured chat UI with LangChain/LangGraph integration out of the box |
| Gradio | `gr.ChatInterface()` for rapid prototyping |
| Panel | `pn.chat` module for data-app-style chat |

---

### Human-in-the-Loop

Pause execution for user approval or input mid-graph.

| Framework | How |
|-----------|-----|
| LangGraph | `interrupt_before` / `interrupt_after` on nodes, `Command(resume=...)` to continue |
| Chainlit | `cl.AskUserMessage()` pauses agent and waits for user response |
| CrewAI | `human_input=True` on task definition prompts user before proceeding |
| AutoGen | `HumanProxyAgent` acts as a human participant in multi-agent conversations |

---

### Dynamic Routing

Conditional graph paths based on intermediate results.

| Framework | How |
|-----------|-----|
| LangGraph | `add_conditional_edges(node, router_fn, {condition: target})` |
| LangGraph | `Command(goto="node_name")` for dynamic routing from within a node |
| CrewAI | Conditional task dependencies with `context` parameter |
| Prefect | `@flow` with `if/else` branching and `task.submit()` for dynamic DAGs |

---

### Tool Use (Function Calling)

Let agents call tools dynamically instead of receiving pre-fetched data.

| Framework | How |
|-----------|-----|
| LangChain | `llm.bind_tools([tool1, tool2])` for OpenAI-compatible function calling |
| LangGraph | `ToolNode(tools)` auto-executes tool calls from LLM responses |
| CrewAI | `@tool` decorator, assign tools per agent |
| AutoGen | Register functions as tools on `AssistantAgent` |
| Anthropic SDK | `tools` parameter in Messages API with auto tool execution via `tool_runner` |
| MCP | Model Context Protocol — expose tools as MCP servers, any client can use them |

---

### Streaming Tokens

Real-time token output instead of waiting for full response.

| Framework | How |
|-----------|-----|
| LangGraph | `stream_mode="messages"` for token-level, `"updates"` for node-level |
| LangChain | `llm.stream(prompt)` returns token iterator |
| FastAPI | `StreamingResponse` with SSE for HTTP clients |
| Vercel AI SDK | `streamText()` / `streamObject()` for React frontends |
| Chainlit | Built-in streaming with `cl.Message(content="").stream_token()` |

---

### Error Recovery / Retry

Graceful retries when agents fail.

| Framework | How |
|-----------|-----|
| LangGraph | `RetryPolicy(max_attempts=3)` on node config |
| tenacity | `@retry(stop=stop_after_attempt(3), wait=wait_exponential())` decorator |
| LangChain | `llm.with_retry(stop_after_attempt=3)` wraps any LLM |
| Prefect | `@task(retries=3, retry_delay_seconds=10)` built into task definition |

---

## Infrastructure

### Checkpointing

Save and resume interrupted graph executions.

| Framework | How |
|-----------|-----|
| LangGraph | `SqliteSaver` (local), `PostgresSaver` (production), `MemorySaver` (dev) |
| LangGraph | `graph.get_state(thread_id)` to inspect, `graph.update_state()` to modify |
| Prefect | Task state persistence with result caching and flow resumption |
| Temporal | Durable execution with automatic state persistence and replay |
| Dagster | Asset-based checkpointing with `@asset` materialization |

---

### Async Execution

True async for better parallelism and throughput.

| Framework | How |
|-----------|-----|
| LangGraph | `async def` node functions, `await graph.ainvoke()` |
| LangChain | `await llm.ainvoke(prompt)` for non-blocking LLM calls |
| httpx | `httpx.AsyncClient()` for async HTTP (replaces `requests`) |
| asyncio | `asyncio.gather()` for concurrent tool calls within a node |
| uvloop | Drop-in event loop replacement for 2-4x faster async |

---

### LLM Response Caching

Avoid redundant LLM calls for identical inputs.

| Framework | How |
|-----------|-----|
| LangChain | `set_llm_cache(SQLiteCache())` — global cache for all LLM calls |
| LangChain | `RedisCache` or `GPTCache` for distributed/semantic caching |
| LiteLLM | Built-in caching layer with Redis/S3 backends |
| Momento | Serverless cache with TTL, integrates with LangChain |
| Custom | Hash prompt → check cache → call LLM → store result |

---

### API Layer

REST/WebSocket API for non-CLI clients.

| Framework | How |
|-----------|-----|
| FastAPI | `@app.post("/analyze")` wraps Runner, `StreamingResponse` for SSE |
| LangServe | `add_routes(app, chain)` auto-generates REST API from any LangChain runnable |
| LangGraph Platform | Managed deployment with built-in API, auth, and scaling |
| Chainlit | Chat UI + API in one, deploy as web app |
| gRPC | High-performance RPC for service-to-service agent communication |

---

### Multi-Model Routing

Different models for different agents based on task complexity.

| Framework | How |
|-----------|-----|
| LangChain | Create multiple `ChatOpenAI` instances with different `model` configs |
| LiteLLM | Unified interface across 100+ providers, `completion(model="gpt-4")` |
| OpenRouter | Single API key, route to any model (OpenAI, Anthropic, Llama, etc.) |
| Vercel AI Gateway | Model routing with failover, cost tracking, rate limiting |
| Custom | Router function selects model based on agent type or task complexity |

---

## Production

### Evaluation Framework

Measure agent quality over time.

| Framework | How |
|-----------|-----|
| LangSmith | `evaluate()` with custom evaluators, dataset-driven testing |
| Ragas | RAG-specific metrics: faithfulness, answer relevancy, context precision |
| DeepEval | `assert_test()` for LLM output quality with 14+ metrics |
| Phoenix (Arize) | Trace-based evaluation with LLM-as-judge |
| Braintrust | Eval framework with scoring, comparison, and regression detection |
| promptfoo | Config-driven prompt testing across models with assertions |

---

### Guardrails

Input/output validation and content filtering.

| Framework | How |
|-----------|-----|
| LangChain | `llm.with_structured_output(PydanticModel)` for schema-enforced responses |
| Guardrails AI | `Guard.from_pydantic(Model)` wraps LLM calls with validation + retry |
| NeMo Guardrails | Colang-based rules for topic control, content filtering, fact-checking |
| Instructor | `client.chat.completions.create(response_model=Model)` with auto-retry |
| Pydantic | Manual `parse_json_response()` + `Model.model_validate()` (what we do now) |

---

### Token Budget Management

Track and limit token usage per run.

| Framework | How |
|-----------|-----|
| LangChain | `get_openai_callback()` context manager tracks tokens and cost per call |
| LiteLLM | Built-in budget tracking with `max_budget` per user/project |
| OpenTelemetry | Custom span attributes for token counts, aggregate in Phoenix |
| Helicone | Proxy that logs all LLM calls with cost, latency, tokens |
| Custom | Callback handler that sums `usage.total_tokens` and raises on budget exceeded |

---

### User / Session Management

Multi-user support with isolated sessions.

| Framework | How |
|-----------|-----|
| LangGraph | `thread_id` in config isolates state per session/user |
| mem0 | `user_id` parameter already partitions memory per user |
| Zep | Session management with user profiles, conversation history, fact extraction |
| Supabase | Auth + Row Level Security for multi-tenant data isolation |
| Clerk | Drop-in auth with user management, integrates with Next.js/FastAPI |

---

### Webhook / Event Hooks

Extensibility points for external integrations.

| Framework | How |
|-----------|-----|
| LangGraph | `on_chain_start` / `on_chain_end` callbacks on nodes |
| LangChain | Custom `BaseCallbackHandler` for any event (LLM start, tool call, error) |
| FastAPI | `BackgroundTasks` to fire webhooks after API response |
| Celery | Task queue for async post-processing (email, Slack, DB writes) |
| Inngest | Event-driven functions with retry, throttling, and fan-out |

---

### Observability (Extended)

Beyond what we have now.

| Framework | How |
|-----------|-----|
| Phoenix (Arize) | Already integrated — LLM traces, evals, embeddings visualization |
| LangFuse | Open-source LLM observability with cost tracking and prompt management |
| Helicone | LLM proxy with logging, caching, rate limiting, cost dashboard |
| Datadog LLM | APM + LLM monitoring with prompt/response capture |
| Weights & Biases | `wandb.init()` + Trace logging for experiment tracking |
| OpenLIT | OpenTelemetry-native LLM monitoring with GPU metrics |
