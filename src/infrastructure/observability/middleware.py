"""Middleware para monitorar requisições HTTP."""
import time
from typing import Callable, Dict, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from infrastructure.observability.metrics import (
    increment_error, increment_internal_request,
    record_internal_request_duration)
from infrastructure.observability.telemetry import create_span


class TelemetryMiddleware(BaseHTTPMiddleware):
    """Middleware para telemetria de requisições HTTP."""

    def __init__(self, app: ASGIApp) -> None:
        """
        Inicializa o middleware.
        
        Args:
            app: Aplicação ASGI
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa a requisição e coleta métricas.
        
        Args:
            request: Requisição HTTP
            call_next: Próxima função a ser chamada no pipeline de middlewares
            
        Returns:
            Response: Resposta HTTP
        """
        # Extrai informações da requisição
        method = request.method
        route = request.url.path
        
        # Registra o início da requisição usando perf_counter para maior precisão e eficiência
        start_time = time.perf_counter()
        
        # Cria um span para a requisição
        attributes = {
            "http.method": method,
            "http.route": route,
            "http.flavor": request.scope.get("http_version", ""),
            "http.user_agent": request.headers.get("user-agent", ""),
        }
        
        # Incrementa o contador de requisições internas
        increment_internal_request(endpoint=route, method=method)
        
        # Cria um span para a requisição
        span_name = f"{method} {route}"
        create_span(span_name, attributes)
        
        try:
            # Processa a requisição
            response = await call_next(request)
            
            # Registra o fim da requisição
            duration = time.perf_counter() - start_time
            duration_ms = duration * 1000
            
            # Atualiza métricas
            record_internal_request_duration(endpoint=route, method=method, duration_ms=duration_ms)
            
            return response
        except Exception as e:
            # Registra erros
            increment_error(error_type=type(e).__name__, endpoint=route)
            raise e