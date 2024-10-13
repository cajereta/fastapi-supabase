from typing import List, Union
from fastapi import Depends, FastAPI
from db import db_connect
from dotenv import dotenv_values
from middleware import get_current_user
from fastapi.middleware.cors import CORSMiddleware

engine, connection = db_connect()

# Secret keys
config = dotenv_values("./.env")
SECRET_KEY = config.get("SECRET_JWT")
ALGORITHM = config.get("ALGORITHM")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/emojis", dependencies=[Depends(get_current_user)])
async def get_emojis(current_user: dict = Depends(get_current_user)) -> List[str]:
    return ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣"]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/")
async def get_emojis() -> List[int]:
    return [1, 2, 3, 5, 6, 8, 10, 154]
