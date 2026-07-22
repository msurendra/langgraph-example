"""Runner service that coordinates graph execution."""

from datetime import date

from graph import build_graph
from schemas.state import GraphState, Recommendation
from services.logging import logger
from services.memory import recall_analyses, store_analysis


class Runner:
    def __init__(self, debug: bool = False) -> None:
        self._graph = build_graph().compile(debug=debug)

    def run(self, ticker: str, stream: bool = False) -> Recommendation:
        logger.info("starting analysis", ticker=ticker)

        past = recall_analyses(ticker)
        initial_state = GraphState(ticker=ticker.upper(), past_analyses=past)

        if stream:
            final_state = self._run_streaming(initial_state)
        else:
            final_state = self._graph.invoke(initial_state.model_dump())

        result = GraphState(**final_state)

        if result.recommendation is None:
            raise RuntimeError(f"No recommendation produced for {ticker}")

        logger.info(
            "analysis complete",
            ticker=ticker,
            signal=result.recommendation.signal.value,
            confidence=result.recommendation.confidence,
        )

        summary = (
            f"[{date.today()}] {ticker.upper()}: {result.recommendation.signal.value} "
            f"(confidence: {result.recommendation.confidence:.0%}). "
            f"{result.recommendation.reasoning}"
        )
        store_analysis(ticker, summary)

        return result.recommendation

    def _run_streaming(self, initial_state: GraphState) -> dict:
        final_state = {}
        for event in self._graph.stream(initial_state.model_dump(), stream_mode="updates"):
            for node_name, updates in event.items():
                logger.info("node completed", node=node_name, keys=list(updates.keys()))
            final_state.update(initial_state.model_dump())
            for event_updates in event.values():
                final_state.update(event_updates)
        return final_state

    def visualize(self) -> str:
        return self._graph.get_graph().draw_mermaid()
