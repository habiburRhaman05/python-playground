from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import List
from .postSchema import post
from .commentSchema import comment
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class userCreate(BaseModel):
    name : str
    email:EmailStr

class user (BaseModel):
    id: int
    name:str
    email:EmailStr
    role:UserRole
    posts:List[post] = []
    comments:List[comment] = []

class usercreateRes (BaseModel):
    success: bool
    userData:user
    message:str

class allUsers(BaseModel):
    success:bool
    message:str
    users:List[user] = []

class updateUserPayload(BaseModel):
    name : str | None = None
    email:EmailStr| None = None