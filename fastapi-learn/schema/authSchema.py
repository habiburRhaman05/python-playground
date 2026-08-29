from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import get_db
from models.userModel import User
from utils.pwdlib import get_password_hash,verify_password
import enum
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
# 2. Reference it inside your main response model
class LoginResponse(BaseModel):
    message: str
    statusCode: int
    access_token: str  # 👈 এটি যোগ করা বাধ্যতামূলক
    token_type: str = "bearer"  # 👈 এটি যোগ করা বাধ্যতামূলক
    userData: UserData

class registerResponse(BaseModel):
    message:str
    statusCode:int

class registerPayload(BaseModel):
    email:EmailStr
    password:str
    name:str
    role:UserRole



