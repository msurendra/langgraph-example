"""Shared LLM instance for all agents."""

from langchain_openai import ChatOpenAI

from config import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL

llm = ChatOpenAI(
    base_url=LM_STUDIO_BASE_URL,
    model=LM_STUDIO_MODEL,
    api_key="lm-studio",
    temperature=0.2,
)
