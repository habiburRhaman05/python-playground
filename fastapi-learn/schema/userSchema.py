from pydantic import BaseModel,EmailStr

class userCreate(BaseModel):
    name : str
    email:EmailStr

class userData (BaseModel):
    id: int
    name:str
    email:EmailStr

class usercreateRes (BaseModel):
    success: bool
    userData:userData
    message:str

class allUsers(BaseModel):
    success:bool
    message:str
    users:list[userData]

class updateUserPayload(BaseModel):
    name : str | None = None
    email:EmailStr| None = None