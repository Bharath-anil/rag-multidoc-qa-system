def expand_query(query:str):
    base = query.lower()

    expansions =[
        query,
        f"{base} meaning",
        f"{base} explanation",
        f"{base} concept"
    ]

    return list(set(expansions))