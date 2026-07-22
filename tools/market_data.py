"""Market data retrieval using Yahoo Finance."""

import yfinance as yf

from schemas.state import CompanyInfo, Fundamentals, MarketData
from services.logging import logger


def fetch_market_data(ticker: str) -> MarketData:
    stock = yf.Ticker(ticker)
    info = stock.info
    logger.info("fetched market data", ticker=ticker)

    return MarketData(
        current_price=info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
        previous_close=info.get("previousClose", 0.0),
        market_cap=info.get("marketCap"),
        volume=info.get("volume"),
        fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
        fifty_two_week_low=info.get("fiftyTwoWeekLow"),
    )


def fetch_company_info(ticker: str) -> CompanyInfo:
    stock = yf.Ticker(ticker)
    info = stock.info
    logger.info("fetched company info", ticker=ticker)

    return CompanyInfo(
        name=info.get("shortName", ticker),
        sector=info.get("sector"),
        industry=info.get("industry"),
        summary=info.get("longBusinessSummary"),
    )


def fetch_fundamentals(ticker: str) -> Fundamentals:
    stock = yf.Ticker(ticker)
    info = stock.info
    logger.info("fetched fundamentals", ticker=ticker)

    return Fundamentals(
        pe_ratio=info.get("trailingPE"),
        forward_pe=info.get("forwardPE"),
        peg_ratio=info.get("pegRatio"),
        price_to_book=info.get("priceToBook"),
        dividend_yield=info.get("dividendYield"),
        earnings_growth=info.get("earningsGrowth"),
        revenue_growth=info.get("revenueGrowth"),
        profit_margin=info.get("profitMargins"),
        debt_to_equity=info.get("debtToEquity"),
        return_on_equity=info.get("returnOnEquity"),
    )
