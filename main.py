import logging
from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException, Request
import os
import jwt
from fastapi.middleware.cors import CORSMiddleware

SECRET_KEY = os.getenv("SECRET_JWT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Make sure your frontend domain is allowed here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(SECRET_KEY)


def format_token(token: str) -> str:
    token = token.replace("-", "+").replace("_", "/")
    return token + "=" * (4 - len(token) % 4)


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


@app.get("/emojis", dependencies=[Depends(get_current_user)])
async def get_emojis(current_user: dict = Depends(get_current_user)) -> List[str]:
    return ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣"]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/")
async def get_emojis() -> List[int]:
    return [1, 2, 3, 5, 6, 8, 10, 154]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
