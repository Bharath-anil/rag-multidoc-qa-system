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
        overlap_sentences = 2
        start = max(i - overlap_sentences, 0)

    chunks = [c for c in chunks if len(c) > 150]
    return chunks
