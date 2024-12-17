import logging

# from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.api.database import create_tables, get_session
from infrastructure.api.routers import (cart_item_routers, product_routers,
                                        user_routers)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(user_routers.router)
app.include_router(product_routers.router)
app.include_router(cart_item_routers.router)

create_tables()
