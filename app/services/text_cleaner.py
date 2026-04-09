import re

def clean_data(text):

    # normalize line endings
    text = text.replace("\r\n", "\n")
    
    # collapse single newlines only
    text = re.sub(r"\n{2,}", "\n", text)

    text = re.sub(r'\(cid:\d+\)', ' ', text)
    text = re.sub(r'Page\s*[-–]?\s*\d+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\.{3,}', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'www\.\S+', ' ', text)
    text = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', ' ', text)
    text = re.sub(r'Clear-Cut Computing.*', ' ', text)
    return text.strip()