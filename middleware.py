from fastapi import HTTPException, Request
from dotenv import dotenv_values
import jwt

config = dotenv_values("./.env")
SECRET_KEY = config.get("SECRET_JWT")


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"], audience="authenticated"
            )
            email = payload.get("user_metadata", {}).get("email")
            role = payload.get("role")
            if email is None or role is None:
                raise HTTPException(status_code=403, detail="Invalid token payload")
            return {"email": email, "role": role}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid JWT token")
    else:
        raise HTTPException(status_code=403, detail="Authorization header missing")
