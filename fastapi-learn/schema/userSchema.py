from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import List,ForwardRef

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class userCreate(BaseModel):
    name : str
    email:EmailStr

class User(BaseModel):
    id: int
    name:str
    email:EmailStr
    role:UserRole
    posts:List["post"] = []
    comments:List["comment"] = []

class usercreateRes (BaseModel):
    success: bool
    userData:User
    message:str

class allUsers(BaseModel):
    success:bool
    message:str
    users:List["User"] = []

class updateUserPayload(BaseModel):
    name : str | None = None
    email:EmailStr| None = None

from schema.postSchema import post
from schema.commentSchema import comment
User.model_rebuild()