from pydantic import BaseModel
from userSchema import user
from postSchema import post
class like(BaseModel):
    id:int
    user:user
    post:post
