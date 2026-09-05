from pydantic import BaseModel,ConfigDict
from userSchema import userData
from likeSchema import like
from commentSchema import comment
from typing import List
class post(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id:int
    title:str
    content:str
    thumbnail:str
    author:userData
    comments: List[comment] = []
    like: List[like] = []
