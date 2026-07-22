"""News sentiment analysis agent."""

from schemas.state import AgentAnalysis, GraphState, Signal
from services.llm import llm
from services.logging import logger
from services.parsing import parse_json_response
from services.prompt import load_prompt


def run_news_agent(state: GraphState) -> AgentAnalysis:
    logger.info("running news agent", ticker=state.ticker)

    news_text = "\n".join(
        f"- {item.title}: {item.snippet[:200]}" for item in state.news_items[:5]
    ) or "No recent news available."

    prompt = load_prompt("news").format(
        ticker=state.ticker,
        company_name=state.company_info.name if state.company_info else state.ticker,
        news_items=news_text,
    )

    response = llm.invoke(prompt)
    parsed = parse_json_response(response.content)

    return AgentAnalysis(
        signal=Signal(parsed["signal"]),
        confidence=parsed["confidence"],
        reasoning=parsed["reasoning"],
    )
