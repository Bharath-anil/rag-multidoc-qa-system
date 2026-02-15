def chunk_data(data, size=900, overlap=100):
    chunks = []
    start = 0

    while start < len(data):
        end = start + size
        chunks.append(data[start:end])
        start += size - overlap

    return chunks