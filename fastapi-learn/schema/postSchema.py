from pydantic import BaseModel, ConfigDict
from typing import List

class post(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    thumbnail: str
    author: "User"           
    comments: List["comment"] = []

class postPayload(BaseModel):
    title: str
    content: str
    thumbnail: str


from schema.userSchema import User
from schema.commentSchema import comment
# 4. Rebuild the model
post.model_rebuild()
