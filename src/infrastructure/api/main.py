import os
import threading

from fastapi import FastAPI

from infrastructure.api.consumers.order_consumer import start_consumer
from infrastructure.api.database import create_tables
from infrastructure.api.routers import (cart_item_routers, cart_routers,
                                        database_routers, offer_routers,
                                        order_routers, payment_routers,
                                        product_routers, user_routers)
from infrastructure.observability.middleware import TelemetryMiddleware
from infrastructure.observability.telemetry import setup_telemetry

app = FastAPI()

# Configuração do OpenTelemetry
tracer_provider = setup_telemetry(app)

# Adiciona o middleware de telemetria
app.add_middleware(TelemetryMiddleware)

app.include_router(user_routers.router)
app.include_router(product_routers.router)
app.include_router(cart_item_routers.router)
app.include_router(cart_routers.router)
app.include_router(offer_routers.router)
app.include_router(payment_routers.router)
app.include_router(order_routers.router)
app.include_router(database_routers.router)

@app.on_event("startup")
async def startup_event():
    await create_tables()
    thread = threading.Thread(target=start_consumer, args=("order_updates",), daemon=True)
    thread.start()

@app.get("/")
def read_root():
    return {"message": "API is running"}