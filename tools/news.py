"""News retrieval using DuckDuckGo Search."""

from ddgs import DDGS

from schemas.state import NewsItem
from services.logging import logger


def fetch_news(ticker: str, max_results: int = 5) -> list[NewsItem]:
    logger.info("fetching news", ticker=ticker, max_results=max_results)

    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(f"{ticker} stock", max_results=max_results))
    except Exception as e:
        logger.warning("news fetch failed, continuing without news", error=str(e))
        return []

    return [
        NewsItem(
            title=r.get("title", ""),
            snippet=r.get("body", ""),
            source=r.get("source"),
        )
        for r in results
    ]
