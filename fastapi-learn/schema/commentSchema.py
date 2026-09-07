from pydantic import BaseModel,ConfigDict
class comment(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id:int
    content:str
    react:int
    author:"User"
    post: "post"


from schema.userSchema import User
from schema.postSchema import post

comment.model_rebuild()