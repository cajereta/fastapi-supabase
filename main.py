from typing import List
from fastapi import Depends, FastAPI

import jwt
from fastapi.middleware.cors import CORSMiddleware

from middleware import get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Make sure your frontend domain is allowed here
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
