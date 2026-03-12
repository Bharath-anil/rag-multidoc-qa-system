import re

def clean_data(text):

    # normalize line endings
    text = text.replace("\r\n", "\n")
    
    # collapse single newlines only
    text = re.sub(r"\n", "\n\n", text)

    text = re.sub(r'\(cid:\d+\)', ' ', text)
    text = re.sub(r'Page\s*[-–]?\s*\d+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\.{3,}', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()