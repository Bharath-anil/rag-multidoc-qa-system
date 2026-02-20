from fastapi import FastAPI
from .routers import upload
from dotenv import load_dotenv
import os

app = FastAPI()
app.include_router(upload.router)
load_dotenv()