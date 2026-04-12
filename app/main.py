from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import upload, query
from app.core.dependencies import vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_store.load_index()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(upload.router)
app.include_router(query.router)