import os
from fastapi import HTTPException, Request
import jwt
import logging

from utils import format_token

SECRET_KEY = os.getenv("SECRET_JWT")


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        token = format_token(token)
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"], audience="authenticated"
            )
            logging.info(f"Decoded payload: {payload}")
            email = payload.get("user_metadata", {}).get("email")
            role = payload.get("role")
            if email is None or role is None:
                raise HTTPException(status_code=403, detail="Invalid token payload")
            return {"email": email, "role": role}
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            raise HTTPException(status_code=403, detail="Token has expired")
        except jwt.InvalidTokenError:
            logging.error("Invalid JWT token")
            raise HTTPException(status_code=403, detail="Invalid JWT token")
    else:
        logging.error("Authorization header missing")
        raise HTTPException(status_code=403, detail="Authorization header missing")
