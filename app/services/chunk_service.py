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

        chunks.append(current.strip())

        # move start forward with overlap
        move = max(1, i - start)
        start += max(1, move - int(overlap / 100))  # simple overlap control

    chunks = [c for c in chunks if len(c) > 150]
    return chunks
