from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="DB Migration API", lifespan=lifespan)
