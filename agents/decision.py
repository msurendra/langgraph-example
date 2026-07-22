"""Decision agent that synthesizes all analyses."""

from schemas.state import GraphState, Recommendation, Signal
from services.llm import llm
from services.logging import logger
from services.parsing import parse_json_response
from services.prompt import load_prompt


def run_decision_agent(state: GraphState) -> Recommendation:
    logger.info("running decision agent", ticker=state.ticker)

    past_text = "\n".join(f"- {m}" for m in state.past_analyses) if state.past_analyses else "No prior analyses."

    prompt = load_prompt("decision").format(
        ticker=state.ticker,
        company_name=state.company_info.name if state.company_info else state.ticker,
        technical_analysis=state.technical_analysis.model_dump_json() if state.technical_analysis else "{}",
        fundamental_analysis=state.fundamental_analysis.model_dump_json() if state.fundamental_analysis else "{}",
        news_analysis=state.news_analysis.model_dump_json() if state.news_analysis else "{}",
        past_analyses=past_text,
    )

    response = llm.invoke(prompt)
    parsed = parse_json_response(response.content)

    return Recommendation(
        signal=Signal(parsed["signal"]),
        confidence=parsed["confidence"],
        reasoning=parsed["reasoning"],
        technical_summary=parsed["technical_summary"],
        fundamental_summary=parsed["fundamental_summary"],
        news_summary=parsed["news_summary"],
    )
