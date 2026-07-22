"""LangGraph workflow definition."""

from langgraph.graph import END, StateGraph

from agents.decision import run_decision_agent
from agents.fundamental import run_fundamental_agent
from agents.news import run_news_agent
from agents.technical import run_technical_agent
from schemas.state import GraphState
from services.logging import logger
from tools.indicators import calculate_indicators
from tools.market_data import fetch_company_info, fetch_fundamentals, fetch_market_data
from tools.news import fetch_news


def collect_data(state: GraphState) -> dict:
    logger.info("collecting data", ticker=state.ticker)
    return {
        "market_data": fetch_market_data(state.ticker),
        "company_info": fetch_company_info(state.ticker),
        "fundamentals": fetch_fundamentals(state.ticker),
        "technical_indicators": calculate_indicators(state.ticker),
        "news_items": fetch_news(state.ticker),
    }


def analyze_technical(state: GraphState) -> dict:
    return {"technical_analysis": run_technical_agent(state)}


def analyze_fundamental(state: GraphState) -> dict:
    return {"fundamental_analysis": run_fundamental_agent(state)}


def analyze_news(state: GraphState) -> dict:
    return {"news_analysis": run_news_agent(state)}


def make_decision(state: GraphState) -> dict:
    return {"recommendation": run_decision_agent(state)}


def build_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("collect_data", collect_data)
    graph.add_node("analyze_technical", analyze_technical)
    graph.add_node("analyze_fundamental", analyze_fundamental)
    graph.add_node("analyze_news", analyze_news)
    graph.add_node("make_decision", make_decision)

    graph.set_entry_point("collect_data")

    graph.add_edge("collect_data", "analyze_technical")
    graph.add_edge("collect_data", "analyze_fundamental")
    graph.add_edge("collect_data", "analyze_news")

    graph.add_edge("analyze_technical", "make_decision")
    graph.add_edge("analyze_fundamental", "make_decision")
    graph.add_edge("analyze_news", "make_decision")

    graph.add_edge("make_decision", END)

    return graph
