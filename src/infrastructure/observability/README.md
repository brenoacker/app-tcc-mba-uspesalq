# Observabilidade com OpenTelemetry

Este módulo implementa observabilidade na aplicação usando OpenTelemetry para monitorar requisições internas e externas, além de operações personalizadas.

## Componentes

- **Telemetria**: Configuração básica do OpenTelemetry e criação de spans
- **Métricas**: Contadores e histogramas para monitorar requisições
- **Middleware**: Middleware para monitorar requisições HTTP
- **Cliente HTTP**: Cliente HTTP instrumentado para monitorar requisições externas
- **Exemplos**: Exemplos de uso da telemetria

## Interfaces de monitoramento

- **Jaeger UI**: http://localhost:16686 - Para visualizar os traces
- **Prometheus**: http://localhost:9090 - Para consultar métricas
- **Grafana**: http://localhost:3000 - Para criar dashboards (usuário: admin, senha: admin)

## Como usar a telemetria

### 1. Monitorar requisições externas

Use o cliente HTTP instrumentado em vez de `requests` ou `httpx` diretamente:

```python
# Em vez de:
import requests
response = requests.get("https://api.example.com")

# Use:
from infrastructure.observability.http_client import InstrumentedHttpClient
response = InstrumentedHttpClient.requests_get("https://api.example.com")


# Para requisições assíncronas:
# Em vez de:
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")

# Use:
from infrastructure.observability.http_client import InstrumentedHttpClient
response = await InstrumentedHttpClient.httpx_get("https://api.example.com")
```

### 2. Criar spans personalizados para operações internas

Para monitorar operações internas, crie spans personalizados:

```python
from infrastructure.observability.telemetry import create_span

# Cria um span para uma operação
with create_span("nome_da_operacao", {"atributo": "valor"}) as span:
    # Código da operação
    resultado = executar_operacao()
    
    # Se quiser registrar uma exceção no span
    try:
        # Operação que pode falhar
        resultado = operacao_arriscada()
    except Exception as e:
        from infrastructure.observability.telemetry import record_exception
        record_exception(e)
        raise e
```

### 3. Monitorar funções específicas

Use o decorador `monitora_funcao` para monitorar funções específicas:

```python
from infrastructure.observability.examples import monitora_funcao

@monitora_funcao
def minha_funcao(arg1, arg2):
    # Código da função
    return resultado
```

### 4. Registrar métricas personalizadas

```python
from infrastructure.observability.metrics import (
    increment_internal_request,
    increment_external_request,
    record_internal_request_duration,
    record_external_request_duration,
    increment_error
)

# Incrementar contador de requisições internas
increment_internal_request(endpoint="/minha-rota", method="GET")

# Registrar duração de uma requisição
record_internal_request_duration(
    endpoint="/minha-rota",
    method="GET",
    duration_ms=150.5
)

# Registrar um erro
increment_error(error_type="ValidationError", endpoint="/minha-rota")
```

## Métricas disponíveis

- **internal_requests**: Contador de requisições internas
- **external_requests**: Contador de requisições externas
- **internal_request_duration**: Histograma de latência de requisições internas
- **external_request_duration**: Histograma de latência de requisições externas
- **errors**: Contador de erros

## Configuração

As configurações da telemetria podem ser ajustadas através de variáveis de ambiente:

- **SERVICE_NAME**: Nome do serviço (padrão: tcc-mba-uspesalq)
- **SERVICE_VERSION**: Versão do serviço (padrão: 0.1.0)
- **OTEL_EXPORTER_OTLP_ENDPOINT**: Endpoint do coletor OpenTelemetry (padrão: http://localhost:4317)
- **PROMETHEUS_PORT**: Porta do servidor HTTP do Prometheus (padrão: 9464) 