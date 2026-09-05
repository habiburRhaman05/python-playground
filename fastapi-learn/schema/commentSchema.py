from pydantic import BaseModel,ConfigDict
from .userSchema import user
from .postSchema import post
class comment(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id:int
    content:str
    react:int
    author:user
    post: post