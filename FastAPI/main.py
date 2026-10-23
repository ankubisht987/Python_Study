from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI()

class Tea(BaseModel):
    id : int
    name: str
    origin: str
    
teas : List[Tea] = []

@app.get("/")
def read_root():
    return {"message" : "Welcome to Chai Code"}

@app.get("/teas")
def get_Teas():
    return teas

@app.post("/teas")
def post_Tea(tea : Tea):
    teas.append(tea)
    return teas

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, update_Tea :Tea):
    for index , tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = update_Tea
            return update_Tea
    return {"Error: ":"Tea not Found"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id : int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted = teas.pop(index)
            return {"Item Deleted : " : deleted}
    return {"Error" : "No Item Exist"}

@app.patch("/teas/{tea_id}")
def patch_tea(tea_id: int , update_tea : Tea):
    for index , tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = update_tea
            return {"This is updated Teas: ": update_tea}
    return{"Error: ":"Tea not Found"}
