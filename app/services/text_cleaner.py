
def clean_data(data):
    cleaned = data.strip().replace("\n ", " ").replace("(cid:127)", "")
    return cleaned