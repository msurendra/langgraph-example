"""Memory service using mem0 for persisting past analyses."""

from mem0 import Memory

from config import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL
from services.logging import logger

_memory: Memory | None = None


def _get_memory() -> Memory:
    global _memory
    if _memory is not None:
        return _memory

    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "model": LM_STUDIO_MODEL,
                "openai_base_url": LM_STUDIO_BASE_URL,
                "api_key": "lm-studio",
                "temperature": 0.1,
            },
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "all-MiniLM-L6-v2",
            },
        },
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "stock_analyses",
                "path": "data/mem0",
            },
        },
    }

    _memory = Memory.from_config(config)
    logger.info("memory service initialized")
    return _memory


def store_analysis(ticker: str, summary: str) -> None:
    try:
        mem = _get_memory()
        mem.add(summary, user_id=ticker.upper())
        logger.info("stored analysis in memory", ticker=ticker)
    except Exception as e:
        logger.warning("failed to store memory, continuing without it", error=str(e))


def recall_analyses(ticker: str, limit: int = 5) -> list[str]:
    try:
        mem = _get_memory()
        results = mem.get_all(filters={"user_id": ticker.upper()})

        memories = [r["memory"] for r in results.get("results", [])][:limit]
        logger.info("recalled memories", ticker=ticker, count=len(memories))
        return memories
    except Exception as e:
        logger.warning("failed to recall memories, continuing without them", error=str(e))
        return []


def search_analyses(query: str, limit: int = 5) -> list[str]:
    try:
        mem = _get_memory()
        results = mem.search(query, limit=limit)
        return [r["memory"] for r in results.get("results", [])]
    except Exception as e:
        logger.warning("failed to search memories", error=str(e))
        return []
