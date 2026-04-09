import re

def chunk_data(text, max_size=800, overlap=150):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    start = 0

    while start < len(sentences):
        current = ""
        i = start

        while i < len(sentences) and len(current) + len(sentences[i]) < max_size:
            current += " " + sentences[i]
            i += 1
        
        if i == start:  
            break

        chunks.append(current.strip())
        overlap_sentences = 2
        next_start = max(i - overlap_sentences, start + 1)  # +1 guarantees forward progress
        start = next_start

    chunks = [c for c in chunks if len(c) > 150]
    return chunks[:10]
