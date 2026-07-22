"""Technical indicator calculations using ta library."""

import pandas as pd
import ta
import yfinance as yf

from schemas.state import TechnicalIndicators
from services.logging import logger


def calculate_indicators(ticker: str, period: str = "6mo") -> TechnicalIndicators:
    logger.info("calculating indicators", ticker=ticker, period=period)

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        logger.warning("no historical data available", ticker=ticker)
        return TechnicalIndicators()

    close: pd.Series = hist["Close"]

    sma_20 = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
    sma_50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None
    sma_200 = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None

    rsi_14 = None
    if len(close) >= 15:
        rsi_series = ta.momentum.rsi(close, window=14)
        rsi_14 = rsi_series.iloc[-1]

    macd_val = None
    macd_sig = None
    if len(close) >= 26:
        macd_indicator = ta.trend.MACD(close)
        macd_val = macd_indicator.macd().iloc[-1]
        macd_sig = macd_indicator.macd_signal().iloc[-1]

    bb_upper = None
    bb_lower = None
    if len(close) >= 20:
        bb = ta.volatility.BollingerBands(close, window=20)
        bb_upper = bb.bollinger_hband().iloc[-1]
        bb_lower = bb.bollinger_lband().iloc[-1]

    return TechnicalIndicators(
        sma_20=_round(sma_20),
        sma_50=_round(sma_50),
        sma_200=_round(sma_200),
        rsi_14=_round(rsi_14),
        macd=_round(macd_val),
        macd_signal=_round(macd_sig),
        bollinger_upper=_round(bb_upper),
        bollinger_lower=_round(bb_lower),
    )


def _round(value: float | None, decimals: int = 2) -> float | None:
    if value is None or pd.isna(value):
        return None
    return round(float(value), decimals)
