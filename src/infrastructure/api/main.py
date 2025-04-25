import asyncio
import os
import threading

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from infrastructure.api.consumers.order_consumer import (start_consumer,
                                                         start_consumer_async)
from infrastructure.api.database import alter_payment_columns, create_tables
from infrastructure.api.routers import (cart_item_routers, cart_routers,
                                        database_routers, offer_routers,
                                        order_routers, payment_routers,
                                        product_routers, user_routers)
from infrastructure.observability.middleware import TelemetryMiddleware
from infrastructure.observability.telemetry import setup_telemetry

# Configurações da aplicação
app = FastAPI(
    title="AckerFood API",
    description="Fast food API for AckerFood",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração do CORS para permitir requisições de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=9)

# Configuração do OpenTelemetry
tracer_provider = setup_telemetry(app)

# Adiciona o middleware de telemetria
app.add_middleware(TelemetryMiddleware)

# Adiciona uma cache de resposta simples para endpoints frequentemente acessados
response_cache = {}

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    # Cache simples para GET requests em endpoints específicos
    if request.method == "GET" and request.url.path in ["/", "/api/health"]:
        cache_key = request.url.path
        if cache_key in response_cache:
            cache_entry = response_cache[cache_key]
            # Cache por 60 segundos
            if cache_entry["timestamp"] + 60 > asyncio.get_event_loop().time():
                return Response(
                    content=cache_entry["content"],
                    status_code=200,
                    media_type="application/json",
                    headers={"X-Cache": "Hit"}
                )
    
    # Processa normalmente para requests não cacheados
    response = await call_next(request)
    
    # Armazena em cache se for um GET para endpoints específicos
    if request.method == "GET" and request.url.path in ["/", "/api/health"]:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        response_cache[request.url.path] = {
            "content": response_body,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return Response(
            content=response_body,
            status_code=response.status_code,
            media_type=response.media_type,
            headers={**dict(response.headers), "X-Cache": "Miss"}
        )
    
    return response

# Registra os routers
app.include_router(user_routers.router)
app.include_router(product_routers.router)
app.include_router(cart_item_routers.router)
app.include_router(cart_routers.router)
app.include_router(offer_routers.router)
app.include_router(payment_routers.router)
app.include_router(order_routers.router)
app.include_router(database_routers.router)

# Variável para armazenar a task do consumer em segundo plano
consumer_task = None

@app.on_event("startup")
async def startup_event():
    """Inicializa componentes na inicialização da aplicação"""
    # Inicializa o banco de dados
    await create_tables()
    await alter_payment_columns()  # Aplica a alteração nas colunas para permitir NULL
    
    # Inicia o consumidor de mensagens em uma thread separada
    # para não bloquear a thread principal que processa requisições HTTP
    thread = threading.Thread(
        target=start_consumer, 
        args=("order_updates",), 
        daemon=True  # Thread daemon encerra quando a thread principal encerra
    )
    thread.start()
    
    # Alternativa: você pode usar start_consumer_async em uma task em segundo plano
    # global consumer_task
    # loop = asyncio.get_event_loop()
    # consumer_task = loop.create_task(start_consumer_async("order_updates"))

@app.on_event("shutdown")
async def shutdown_event():
    """Limpeza ao encerrar a aplicação"""
    # Encerra graciosamente tasks em segundo plano
    global consumer_task
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/api/health")
def health_check():
    """Endpoint para verificação de saúde da API"""
    return {
        "status": "ok",
        "version": "1.0.0"
    }