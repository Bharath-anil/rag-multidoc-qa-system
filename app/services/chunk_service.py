import re

def chunk_data(text, max_size=800, overlap=100):

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for p in paragraphs:
        if len(current_chunk) + len(p) < max_size:
            current_chunk += " " + p
        else:
            chunks.append(current_chunk.strip())
            current_chunk = p

    if current_chunk:
        chunks.append(current_chunk.strip())

    chunks = [c for c in chunks if len(c) > 150]
    return chunks