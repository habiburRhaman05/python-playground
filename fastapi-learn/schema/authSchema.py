from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import get_db
from models.userModel import User
from utils.pwdlib import get_password_hash,verify_password
class user(BaseModel):
    id:int
    email:EmailStr
    password:str
    name:str

class loginPayload(BaseModel):
    email:EmailStr
    password:str

class UserData(BaseModel):
    id: int
    email: EmailStr
    name: str

# 2. Reference it inside your main response model
class LoginResponse(BaseModel):
    userData: UserData
    message: str
    statusCode: int

class registerResponse(BaseModel):
    userData:user
    message:str
    statusCode:int

class registerPayload(BaseModel):
    email:EmailStr
    password:str
    name:str


