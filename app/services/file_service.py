import os
from pathlib import Path


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

document_store ={
    "chunks":[],
    "embeddings":[]
}

def save_file(file):
    file_path = UPLOAD_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path

