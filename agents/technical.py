"""Technical analysis agent."""

from schemas.state import AgentAnalysis, GraphState, Signal
from services.llm import llm
from services.logging import logger
from services.parsing import parse_json_response
from services.prompt import load_prompt


def run_technical_agent(state: GraphState) -> AgentAnalysis:
    logger.info("running technical agent", ticker=state.ticker)

    prompt = load_prompt("technical").format(
        ticker=state.ticker,
        current_price=state.market_data.current_price if state.market_data else "N/A",
        indicators=state.technical_indicators.model_dump_json() if state.technical_indicators else "{}",
    )

    response = llm.invoke(prompt)
    parsed = parse_json_response(response.content)

    return AgentAnalysis(
        signal=Signal(parsed["signal"]),
        confidence=parsed["confidence"],
        reasoning=parsed["reasoning"],
    )
