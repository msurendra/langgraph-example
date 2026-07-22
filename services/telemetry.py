"""OpenTelemetry and OpenInference setup with Phoenix and local file export."""

import json
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult

from config import LOGS_DIR, OTEL_SERVICE_NAME
from services.logging import logger


class FileSpanExporter(SpanExporter):
    def __init__(self, output_dir: Path) -> None:
        self._output_dir = output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._file = open(self._output_dir / "traces.jsonl", "a")

    def export(self, spans: list) -> SpanExportResult:
        for span in spans:
            record = {
                "name": span.name,
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
                "parent_span_id": format(span.parent.span_id, "016x") if span.parent else None,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "status": span.status.status_code.name,
                "attributes": dict(span.attributes) if span.attributes else {},
            }
            self._file.write(json.dumps(record, default=str) + "\n")
        self._file.flush()
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        self._file.close()


def setup_telemetry() -> None:
    resource = Resource.create({"service.name": OTEL_SERVICE_NAME})
    provider = TracerProvider(resource=resource)

    file_exporter = FileSpanExporter(LOGS_DIR)
    provider.add_span_processor(BatchSpanProcessor(file_exporter))

    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        phoenix_exporter = OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
        provider.add_span_processor(BatchSpanProcessor(phoenix_exporter))
        logger.info("phoenix exporter enabled", endpoint="http://localhost:6006")
    except Exception as e:
        logger.warning("phoenix exporter not available, using file export only", error=str(e))

    trace.set_tracer_provider(provider)

    try:
        from openinference.instrumentation.langchain import LangChainInstrumentor
        LangChainInstrumentor().instrument()
        logger.info("openinference langchain instrumentation enabled")
    except Exception as e:
        logger.warning("openinference instrumentation failed", error=str(e))

    logger.info("telemetry initialized")
