"""Graph state and shared Pydantic models."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Signal(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class MarketData(BaseModel):
    current_price: float
    previous_close: float
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None


class CompanyInfo(BaseModel):
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None


class Fundamentals(BaseModel):
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_growth: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    return_on_equity: Optional[float] = None


class TechnicalIndicators(BaseModel):
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None


class NewsItem(BaseModel):
    title: str
    snippet: str
    source: Optional[str] = None


class AgentAnalysis(BaseModel):
    signal: Signal
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class Recommendation(BaseModel):
    signal: Signal
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    technical_summary: str
    fundamental_summary: str
    news_summary: str


class GraphState(BaseModel):
    ticker: str
    market_data: Optional[MarketData] = None
    company_info: Optional[CompanyInfo] = None
    fundamentals: Optional[Fundamentals] = None
    technical_indicators: Optional[TechnicalIndicators] = None
    news_items: list[NewsItem] = Field(default_factory=list)
    technical_analysis: Optional[AgentAnalysis] = None
    fundamental_analysis: Optional[AgentAnalysis] = None
    news_analysis: Optional[AgentAnalysis] = None
    past_analyses: list[str] = Field(default_factory=list)
    recommendation: Optional[Recommendation] = None
