import re

def chunk_data(text, max_size=800, overlap=150):

    chunks =[]
    start =0

    while start <= len(text):
        end =start + max_size
        chunk =text[start:end]
        chunks.append(chunk.strip())

        start += (max_size - overlap)

    chunks =[c for c in chunks if len(c)>150]
    return chunks