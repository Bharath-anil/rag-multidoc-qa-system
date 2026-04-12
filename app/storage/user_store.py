users = {}

def create_user(username: str):
    if username in users:
        return users[username]

    users[username] = {
        "username": username,
        "documents": []
    }
    return users[username]


def get_user(username: str):
    return users.get(username)