import os
from pathlib import Path
from . import text_extractor

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(file):
    file_path = UPLOAD_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path

def process_file(file):
    file_path = save_file(file)
    return text_extractor.extract_text(file_path)