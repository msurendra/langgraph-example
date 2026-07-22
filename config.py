"""Centralized application configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env.local")

LM_STUDIO_BASE_URL: str = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_MODEL: str = os.getenv("LM_STUDIO_MODEL", "google/gemma-4-12b-qat")

LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "langgraph-example")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME", "langgraph-example")
OTEL_EXPORTER_OTLP_ENDPOINT: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

PROMPTS_DIR: Path = BASE_DIR / "prompts"
LOGS_DIR: Path = BASE_DIR / "logs"
DATA_DIR: Path = BASE_DIR / "data"
