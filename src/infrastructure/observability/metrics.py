"""Módulo para métricas personalizadas da aplicação."""
import os
from typing import Any, Dict, List, Optional

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

# Constantes para o serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "tcc-mba-uspesalq")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1.0")

# Cria o resource com informações do serviço
resource = Resource.create({
    "service.name": SERVICE_NAME,
    "service.version": SERVICE_VERSION,
})

# Obtém o meter provider global
meter = metrics.get_meter(__name__)

# Contadores para requisições internas e externas
internal_request_counter = meter.create_counter(
    name="internal_requests",
    description="Contador de requisições internas",
    unit="1",
)

external_request_counter = meter.create_counter(
    name="external_requests",
    description="Contador de requisições externas",
    unit="1",
)

# Histogramas para latência de requisições
internal_request_duration = meter.create_histogram(
    name="internal_request_duration",
    description="Latência das requisições internas",
    unit="ms",
)

external_request_duration = meter.create_histogram(
    name="external_request_duration",
    description="Latência das requisições externas",
    unit="ms",
)

# Contadores para erros
error_counter = meter.create_counter(
    name="errors",
    description="Contador de erros",
    unit="1",
)

# Funções para incrementar os contadores

def increment_internal_request(endpoint: str, method: str) -> None:
    """
    Incrementa o contador de requisições internas.
    
    Args:
        endpoint: Endpoint da requisição
        method: Método HTTP da requisição
    """
    internal_request_counter.add(1, {"endpoint": endpoint, "method": method})

def increment_external_request(service: str, endpoint: str, method: str) -> None:
    """
    Incrementa o contador de requisições externas.
    
    Args:
        service: Nome do serviço externo
        endpoint: Endpoint da requisição
        method: Método HTTP da requisição
    """
    external_request_counter.add(1, {"service": service, "endpoint": endpoint, "method": method})

def record_internal_request_duration(endpoint: str, method: str, duration_ms: float) -> None:
    """
    Registra a duração de uma requisição interna.
    
    Args:
        endpoint: Endpoint da requisição
        method: Método HTTP da requisição
        duration_ms: Duração da requisição em milissegundos
    """
    internal_request_duration.record(duration_ms, {"endpoint": endpoint, "method": method})

def record_external_request_duration(service: str, endpoint: str, method: str, duration_ms: float) -> None:
    """
    Registra a duração de uma requisição externa.
    
    Args:
        service: Nome do serviço externo
        endpoint: Endpoint da requisição
        method: Método HTTP da requisição
        duration_ms: Duração da requisição em milissegundos
    """
    external_request_duration.record(duration_ms, {"service": service, "endpoint": endpoint, "method": method})

def increment_error(error_type: str, endpoint: Optional[str] = None) -> None:
    """
    Incrementa o contador de erros.
    
    Args:
        error_type: Tipo de erro
        endpoint: Endpoint onde ocorreu o erro (opcional)
    """
    attributes = {"error_type": error_type}
    if endpoint:
        attributes["endpoint"] = endpoint
    
    error_counter.add(1, attributes) 