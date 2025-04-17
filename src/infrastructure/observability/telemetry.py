"""OpenTelemetry configuration for the application."""
import os
from typing import Dict, Optional

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import start_http_server

# Constantes para o serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "tcc-mba-uspesalq")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1.0")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9464"))

# Cria o resource com informações do serviço
resource = Resource.create({
    "service.name": SERVICE_NAME,
    "service.version": SERVICE_VERSION,
})

def setup_telemetry(app: FastAPI) -> None:
    """
    Configura o OpenTelemetry para a aplicação FastAPI.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Configuração do tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    
    # Configuração do exportador OTLP
    otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    
    # Configuração do exportador Prometheus para métricas
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
    
    # Inicia o servidor HTTP do Prometheus
    start_http_server(PROMETHEUS_PORT)
    
    # Instrumentação do FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrumentação para requisições HTTP externas
    RequestsInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()

    return tracer_provider

def create_span(name: str, attributes: Optional[Dict] = None) -> None:
    """
    Cria um span personalizado para monitorar uma operação específica.
    
    Args:
        name: Nome do span
        attributes: Atributos adicionais do span
    """
    tracer = trace.get_tracer(__name__)
    attributes = attributes or {}
    
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, value)
            
def record_exception(exception: Exception) -> None:
    """
    Registra uma exceção no span atual.
    
    Args:
        exception: Exceção a ser registrada
    """
    current_span = trace.get_current_span()
    current_span.record_exception(exception)
    current_span.set_status(trace.Status(trace.StatusCode.ERROR)) 