from pydantic import BaseModel
# from pydantic import *
# import pydantic

class User(BaseModel):
    id: int 
    name : str
    is_active : bool

value = {'id': "10005" , "name" : "Ankush" , "is_active" : True}
result = User(**value)
print(result)