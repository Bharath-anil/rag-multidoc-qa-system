from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from app.routers import auth
from app.routers import upload, query,document,conversation_router
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import (http_exception_handler, validation_exception_handler,general_exception_handler,)
from fastapi.exceptions import RequestValidationError
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler# type: ignore[arg-type]
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler# type: ignore[arg-type]
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(document.router)
app.include_router(conversation_router.router)