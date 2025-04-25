"""Cliente HTTP instrumentado com OpenTelemetry."""
import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

import httpx
import requests
from opentelemetry import trace

from infrastructure.observability.metrics import (increment_error,
                                                   increment_external_request,
                                                   record_external_request_duration)
from infrastructure.observability.telemetry import create_span, record_exception


class InstrumentedHttpClient:
    """Cliente HTTP instrumentado com OpenTelemetry."""
    
    @staticmethod
    def _extract_service_and_endpoint(url: str) -> tuple:
        """
        Extrai o serviço e o endpoint de uma URL.
        
        Args:
            url: URL da requisição
            
        Returns:
            tuple: (service, endpoint)
        """
        parsed_url = urlparse(url)
        service = parsed_url.netloc
        endpoint = parsed_url.path
        return service, endpoint
    
    @staticmethod
    def requests_get(url: str, **kwargs) -> requests.Response:
        """
        Faz uma requisição GET usando a biblioteca requests.
        
        Args:
            url: URL da requisição
            **kwargs: Argumentos adicionais para a função requests.get
            
        Returns:
            requests.Response: Resposta da requisição
        """
        service, endpoint = InstrumentedHttpClient._extract_service_and_endpoint(url)
        method = "GET"
        
        # Registra o início da requisição
        start_time = time.time()
        
        # Cria um span para a requisição
        span_name = f"HTTP {method} {service}{endpoint}"
        attributes = {
            "http.method": method,
            "http.url": url,
            "http.service": service,
            "http.endpoint": endpoint,
        }
        create_span(span_name, attributes)
        
        # Incrementa o contador de requisições externas
        increment_external_request(service=service, endpoint=endpoint, method=method)
        
        try:
            # Faz a requisição
            response = requests.get(url, **kwargs)
            
            # Registra métricas
            duration = time.time() - start_time
            duration_ms = duration * 1000
            record_external_request_duration(
                service=service, 
                endpoint=endpoint, 
                method=method, 
                duration_ms=duration_ms
            )
            
            return response
        except Exception as e:
            # Registra erros
            increment_error(error_type=type(e).__name__, endpoint=f"{service}{endpoint}")
            record_exception(e)
            raise e
    
    @staticmethod
    def requests_post(url: str, **kwargs) -> requests.Response:
        """
        Faz uma requisição POST usando a biblioteca requests.
        
        Args:
            url: URL da requisição
            **kwargs: Argumentos adicionais para a função requests.post
            
        Returns:
            requests.Response: Resposta da requisição
        """
        service, endpoint = InstrumentedHttpClient._extract_service_and_endpoint(url)
        method = "POST"
        
        # Registra o início da requisição
        start_time = time.time()
        
        # Cria um span para a requisição
        span_name = f"HTTP {method} {service}{endpoint}"
        attributes = {
            "http.method": method,
            "http.url": url,
            "http.service": service,
            "http.endpoint": endpoint,
        }
        create_span(span_name, attributes)
        
        # Incrementa o contador de requisições externas
        increment_external_request(service=service, endpoint=endpoint, method=method)
        
        try:
            # Faz a requisição
            response = requests.post(url, **kwargs)
            
            # Registra métricas
            duration = time.time() - start_time
            duration_ms = duration * 1000
            record_external_request_duration(
                service=service, 
                endpoint=endpoint, 
                method=method, 
                duration_ms=duration_ms
            )
            
            return response
        except Exception as e:
            # Registra erros
            increment_error(error_type=type(e).__name__, endpoint=f"{service}{endpoint}")
            record_exception(e)
            raise e
    
    @staticmethod
    async def httpx_get(url: str, **kwargs) -> httpx.Response:
        """
        Faz uma requisição GET assíncrona usando a biblioteca httpx.
        
        Args:
            url: URL da requisição
            **kwargs: Argumentos adicionais para a função httpx.AsyncClient.get
            
        Returns:
            httpx.Response: Resposta da requisição
        """
        service, endpoint = InstrumentedHttpClient._extract_service_and_endpoint(url)
        method = "GET"
        
        # Registra o início da requisição
        start_time = time.time()
        
        # Cria um span para a requisição
        span_name = f"HTTP {method} {service}{endpoint}"
        attributes = {
            "http.method": method,
            "http.url": url,
            "http.service": service,
            "http.endpoint": endpoint,
        }
        create_span(span_name, attributes)
        
        # Incrementa o contador de requisições externas
        increment_external_request(service=service, endpoint=endpoint, method=method)
        
        try:
            # Faz a requisição
            async with httpx.AsyncClient() as client:
                response = await client.get(url, **kwargs)
            
            # Registra métricas
            duration = time.time() - start_time
            duration_ms = duration * 1000
            record_external_request_duration(
                service=service, 
                endpoint=endpoint, 
                method=method, 
                duration_ms=duration_ms
            )
            
            return response
        except Exception as e:
            # Registra erros
            increment_error(error_type=type(e).__name__, endpoint=f"{service}{endpoint}")
            record_exception(e)
            raise e
    
    @staticmethod
    async def httpx_post(url: str, **kwargs) -> httpx.Response:
        """
        Faz uma requisição POST assíncrona usando a biblioteca httpx.
        
        Args:
            url: URL da requisição
            **kwargs: Argumentos adicionais para a função httpx.AsyncClient.post
            
        Returns:
            httpx.Response: Resposta da requisição
        """
        service, endpoint = InstrumentedHttpClient._extract_service_and_endpoint(url)
        method = "POST"
        
        # Registra o início da requisição
        start_time = time.time()
        
        # Cria um span para a requisição
        span_name = f"HTTP {method} {service}{endpoint}"
        attributes = {
            "http.method": method,
            "http.url": url,
            "http.service": service,
            "http.endpoint": endpoint,
        }
        create_span(span_name, attributes)
        
        # Incrementa o contador de requisições externas
        increment_external_request(service=service, endpoint=endpoint, method=method)
        
        try:
            # Faz a requisição
            async with httpx.AsyncClient() as client:
                response = await client.post(url, **kwargs)
            
            # Registra métricas
            duration = time.time() - start_time
            duration_ms = duration * 1000
            record_external_request_duration(
                service=service, 
                endpoint=endpoint, 
                method=method, 
                duration_ms=duration_ms
            )
            
            return response
        except Exception as e:
            # Registra erros
            increment_error(error_type=type(e).__name__, endpoint=f"{service}{endpoint}")
            record_exception(e)
            raise e 