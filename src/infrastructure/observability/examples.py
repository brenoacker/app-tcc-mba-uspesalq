"""Exemplos de uso da telemetria e do cliente HTTP instrumentado."""
import time
import asyncio
import requests
import httpx

from infrastructure.observability.http_client import InstrumentedHttpClient
from infrastructure.observability.telemetry import create_span, record_exception
from infrastructure.observability.metrics import (
    increment_internal_request,
    increment_external_request,
    record_internal_request_duration,
    record_external_request_duration,
    increment_error
)

# Exemplo 1: Uso do cliente HTTP instrumentado para requisições síncronas
def exemplo_get_sincrono():
    """Exemplo de uso do cliente HTTP instrumentado para requisições GET síncronas."""
    try:
        # Esta requisição será automaticamente instrumentada
        response = InstrumentedHttpClient.requests_get("https://api.example.com/data")
        return response.json()
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")
        return None

def exemplo_post_sincrono():
    """Exemplo de uso do cliente HTTP instrumentado para requisições POST síncronas."""
    try:
        # Esta requisição será automaticamente instrumentada
        data = {"key": "value"}
        response = InstrumentedHttpClient.requests_post(
            "https://api.example.com/data",
            json=data
        )
        return response.json()
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")
        return None

# Exemplo 2: Uso do cliente HTTP instrumentado para requisições assíncronas
async def exemplo_get_assincrono():
    """Exemplo de uso do cliente HTTP instrumentado para requisições GET assíncronas."""
    try:
        # Esta requisição será automaticamente instrumentada
        response = await InstrumentedHttpClient.httpx_get("https://api.example.com/data")
        return response.json()
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")
        return None

async def exemplo_post_assincrono():
    """Exemplo de uso do cliente HTTP instrumentado para requisições POST assíncronas."""
    try:
        # Esta requisição será automaticamente instrumentada
        data = {"key": "value"}
        response = await InstrumentedHttpClient.httpx_post(
            "https://api.example.com/data",
            json=data
        )
        return response.json()
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")
        return None

# Exemplo 3: Uso de spans personalizados para medir operações internas
def exemplo_span_personalizado():
    """Exemplo de uso de spans personalizados para medir operações internas."""
    # Criando um span personalizado
    with create_span("operacao_personalizada", {"operation.type": "custom"}) as span:
        try:
            # Simulando uma operação que leva tempo
            time.sleep(0.5)
            
            # Registrando métricas personalizadas
            increment_internal_request(endpoint="operacao_personalizada", method="CUSTOM")
            record_internal_request_duration(
                endpoint="operacao_personalizada",
                method="CUSTOM",
                duration_ms=500
            )
            
            # Realizando uma sub-operação com outro span
            with create_span("sub_operacao", {"operation.type": "sub_custom"}) as sub_span:
                time.sleep(0.2)
        except Exception as e:
            # Registrando erros
            record_exception(e)
            increment_error(error_type=type(e).__name__, endpoint="operacao_personalizada")
            raise e

# Exemplo 4: Monitorando uma função específica
def monitora_funcao(func):
    """
    Decorador para monitorar uma função.
    
    Args:
        func: Função a ser monitorada
    """
    def wrapper(*args, **kwargs):
        # Nome do span baseado no nome da função
        span_name = f"func.{func.__name__}"
        
        # Atributos do span
        attributes = {
            "function.name": func.__name__,
            "function.args_count": len(args),
            "function.kwargs_count": len(kwargs)
        }
        
        # Registra o início da função
        start_time = time.time()
        
        # Cria um span para a função
        with create_span(span_name, attributes):
            try:
                # Executa a função
                result = func(*args, **kwargs)
                
                # Registra métricas
                duration = time.time() - start_time
                duration_ms = duration * 1000
                
                # Métricas da função são registradas como requisições internas
                increment_internal_request(endpoint=span_name, method="FUNCTION")
                record_internal_request_duration(
                    endpoint=span_name,
                    method="FUNCTION",
                    duration_ms=duration_ms
                )
                
                return result
            except Exception as e:
                # Registra erros
                increment_error(error_type=type(e).__name__, endpoint=span_name)
                record_exception(e)
                raise e
    
    return wrapper

# Exemplo de uso do decorador
@monitora_funcao
def funcao_monitorada(a, b):
    """Função de exemplo que será monitorada."""
    time.sleep(0.3)  # Simulando uma operação que leva tempo
    return a + b 