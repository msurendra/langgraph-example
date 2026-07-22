"""Fundamental analysis agent."""

from schemas.state import AgentAnalysis, GraphState, Signal
from services.llm import llm
from services.logging import logger
from services.parsing import parse_json_response
from services.prompt import load_prompt


def run_fundamental_agent(state: GraphState) -> AgentAnalysis:
    logger.info("running fundamental agent", ticker=state.ticker)

    prompt = load_prompt("fundamental").format(
        ticker=state.ticker,
        company_name=state.company_info.name if state.company_info else state.ticker,
        sector=state.company_info.sector if state.company_info else "N/A",
        fundamentals=state.fundamentals.model_dump_json() if state.fundamentals else "{}",
    )

    response = llm.invoke(prompt)
    parsed = parse_json_response(response.content)

    return AgentAnalysis(
        signal=Signal(parsed["signal"]),
        confidence=parsed["confidence"],
        reasoning=parsed["reasoning"],
    )
