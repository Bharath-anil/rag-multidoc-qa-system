from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import auth
from app.routers import upload, query
from app.core.dependencies import vector_store
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_store.load_index()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(query.router)