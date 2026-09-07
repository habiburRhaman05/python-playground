from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import get_db


from utils.pwdlib import get_password_hash,verify_password
import enum
from typing import List
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class user(BaseModel):
    id:int
    email:EmailStr
    password:str
    name:str
    role:UserRole

class loginPayload(BaseModel):
    email:EmailStr
    password:str

class UserData(BaseModel):
    id: int
    email: EmailStr
    name: str
    role:UserRole
    token:str | None
    posts:List["post"] = []
# 2. Reference it inside your main response model
class LoginResponse(BaseModel):
    message: str
    statusCode: int
    access_token: str  
    token_type: str = "bearer"  
    userData: UserData

class registerResponse(BaseModel):
    message:str
    statusCode:int

class registerPayload(BaseModel):
    email:EmailStr
    password:str
    name:str
    role:UserRole


class UpdateSchema(BaseModel):
    name:str | None 

from .postSchema import post
from .commentSchema import comment



