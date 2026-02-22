import re
def clean_data(data: str) -> str:
    cleaned = re.sub(r"\(cid:\d+\)", "", data)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()