import pdfplumber

def extract_text(file_path):
    all_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"

    return {
        "filename": file_path.name,
        "text_length": len(all_text),
        "preview": all_text[:500]
    }