from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Play(BaseModel):
    id : int
    item : str
    stock: int

play : List[Play] = []

@app.get("/")
def plays():
    return "Health Check"

@app.get("/play")
def item():
    return play

@app.post("/play")
def item_post(data : Play):
    play.append(data)
    return play
