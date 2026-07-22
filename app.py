"""CLI entry point for stock analysis."""

import argparse
import sys

from rich.console import Console
from rich.panel import Panel

from services.runner import Runner
from services.telemetry import setup_telemetry


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Stock Analyzer")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("--debug", action="store_true", help="Enable LangGraph debug logging")
    parser.add_argument("--stream", action="store_true", help="Stream node-by-node progress")
    parser.add_argument("--visualize", action="store_true", help="Print graph diagram and exit")
    parser.add_argument("--history", action="store_true", help="Show past analyses for ticker and exit")
    args = parser.parse_args()

    console = Console()
    setup_telemetry()

    runner = Runner(debug=args.debug)

    if args.visualize:
        console.print(Panel(runner.visualize(), title="Graph Diagram (Mermaid)"))
        return

    if args.history:
        from services.memory import recall_analyses
        memories = recall_analyses(args.ticker)
        if not memories:
            console.print(f"No past analyses for [bold]{args.ticker.upper()}[/bold].")
        else:
            console.print(Panel(
                "\n".join(memories),
                title=f"Past Analyses: {args.ticker.upper()}",
            ))
        return

    console.print(f"\nAnalyzing [bold]{args.ticker.upper()}[/bold]...\n")

    try:
        recommendation = runner.run(args.ticker, stream=args.stream)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    color = {"BUY": "green", "SELL": "red", "HOLD": "yellow"}[recommendation.signal.value]

    console.print(Panel(
        f"[bold {color}]{recommendation.signal.value}[/bold {color}]"
        f"  (confidence: {recommendation.confidence:.0%})\n\n"
        f"{recommendation.reasoning}\n\n"
        f"[dim]Technical:[/dim] {recommendation.technical_summary}\n"
        f"[dim]Fundamental:[/dim] {recommendation.fundamental_summary}\n"
        f"[dim]News:[/dim] {recommendation.news_summary}",
        title=f"{args.ticker.upper()} Recommendation",
        border_style=color,
    ))


if __name__ == "__main__":
    main()
