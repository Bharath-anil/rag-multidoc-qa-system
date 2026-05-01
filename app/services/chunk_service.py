import re
from collections import Counter
 
# Generic section types to skip — these exist in almost every textbook/doc
SKIP_SECTIONS = re.compile(
    r"^\s*(objectives|terminal exercise|intext questions|what you have learnt|"
    r"answers to intext|fill in the blank|state whether|choose the correct|"
    r"summary|review questions|exercises|activities)\s*$",
    re.IGNORECASE
)
 
# Generic structural noise — pattern based, NOT content based
NOISE_LINE = re.compile(
    r"^\s*("
    r"fig(ure)?\.?\s*\d+[\.\d]*.*|"      # Fig. 1.2: Something
    r"module\s*[-–]\s*\d+|"              # MODULE – 1
    r"\d+\s*$|"                           # lone page number
    r"[a-z ]+\s+\d+\s*$|"               # "Computer Science 3"
    r"\d+\s+[a-z ]+\s*$"                # "3 Computer Science"
    r")\s*$",
    re.IGNORECASE
)
 
def find_repeated_lines(lines, threshold=3):
    """Lines appearing 3+ times are headers/footers — drop them."""
    counts = Counter(l.strip() for l in lines if len(l.strip()) > 2)
    return {line for line, count in counts.items() if count >= threshold}
 
def chunk_data(text, max_size=300, min_size=50):
    lines = text.splitlines()
 
    # Find repeated header/footer lines generically
    repeated = find_repeated_lines(lines)
 
    cleaned = []
    skip_mode = False
 
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
 
        # Skip repeated headers/footers (page headers, footers)
        if stripped in repeated:
            continue
 
        # Enter skip mode on known boilerplate section headers
        if SKIP_SECTIONS.match(stripped):
            skip_mode = True
            continue
 
        if re.match(r'^\d+[\.\d]*\s+\S', stripped):
            skip_mode = False
 
        if skip_mode:
            continue
 
        if NOISE_LINE.match(stripped):
            continue
 
        cleaned.append(stripped)
 
    # Merge into chunks
    chunks = []
    buffer = ""
 
    for line in cleaned:
        if len(buffer) + len(line) + 1 < max_size:
            buffer = (buffer + " " + line).strip()
        else:
            if len(buffer) >= min_size:
                chunks.append(buffer)
            buffer = line
 
    if len(buffer) >= min_size:
        chunks.append(buffer)
    
    def extract_definition_sentences(text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [
            s.strip()
            for s in sentences
            if " is " in s.lower() and 20 < len(s) < 200
        ]


    return chunks + extract_definition_sentences(" ".join(chunks))