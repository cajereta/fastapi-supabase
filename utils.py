def format_token(token: str) -> str:
    token = token.replace("-", "+").replace("_", "/")
    return token + "=" * (4 - len(token) % 4)
