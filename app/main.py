from fastapi import FastAPI
from .routers import upload
from dotenv import load_dotenv
import os
from .services.vector_store_service import load_index

app = FastAPI()
load_dotenv()
load_index()
app.include_router(upload.router)
