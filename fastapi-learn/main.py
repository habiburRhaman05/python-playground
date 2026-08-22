import os
from dotenv import load_dotenv
from fastapi import FastAPI,status,HTTPException,Depends
from routers.books import router as books_router
from sqlalchemy import create_engine, Column, Integer, String,select,delete,update
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel,EmailStr
from typing import Generator
from sqlalchemy.exc import SQLAlchemyError
load_dotenv()
# 1. Database Configuration
# Replace this with your actual Neon connection string (usually kept in a .env file)
DATABASE_URL = os.getenv(
    "DATABASE_URL")

# 2. SQLAlchemy Setup
# Neon requires SSL, which is handled by '?sslmode=require' in the URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


    # This function acts as a session lifecycle manager
def get_db():
    db = SessionLocal() # 1. Open a new database session
    try:
        yield db        # 2. Hand the session over to the endpoint
    finally:
        db.close()

# 3. Database Model (Example: User Table)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.include_router(books_router)

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

@app.get("/")
def read_root():
    return {"message": "Hello World Fasstapi"}


@app.post("/users",response_model=usercreateRes,status_code=status.HTTP_201_CREATED)
def createUser(userPayload:userCreate,db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == userPayload.email)
    existingUser = db.execute(stmt).scalar_one_or_none()
    if existingUser :
        raise HTTPException(status_code=400,detail="email already used")

    new_user = User(
        name = userPayload.name,
        email = userPayload.email
    );

    db.add(new_user);
    db.commit()
    db.refresh(new_user)

    return {
        'success':True,
        'message': 'User created successfully!',
        'userData':new_user
    };



@app.get(
    "/users",
    response_model=allUsers,
    status_code=status.HTTP_200_OK
)
def getAllUsers(db: Session = Depends(get_db)):
    try:
        stmt = select(User)

        users = db.execute(stmt).scalars().all()

        return {
            "success": True,
            "message": "Users fetched successfully",
            "users": users
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )



@app.patch("/users/{id}",response_model=usercreateRes,status_code=status.HTTP_200_OK)
def updateUser(id:int,updatePayload:updateUserPayload,db:Session=Depends(get_db)):
    try:
        existStmt = select(User).where(User.id == id);
        existingUser = db.execute(existStmt).scalar_one_or_none();
        if not existingUser:
          raise HTTPException(
            status_code=404,
            detail="User not found"
        )

        updated_data = updatePayload.model_dump(exclude_unset=True);

        for field,value in updated_data.items():
         setattr(existingUser,field,value)
        db.commit();
        db.refresh(existingUser);
        return {
             "success": True,
                        "message": "Users updated successfully",
                        "userData": existingUser
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="failed to update user data")

@app.delete("/users/{id}",response_model=usercreateRes,status_code=status.HTTP_200_OK)
def updateUser(id:int,db:Session=Depends(get_db)):
    try:
        existStmt = select(User).where(User.id == id);
        existingUser = db.execute(existStmt).scalar_one_or_none();
        if not existingUser:
          raise HTTPException(
            status_code=404,
            detail="User not found"
        )

        deleteStmt = delete(User).where(User.id == id)
        db.execute(deleteStmt)
        db.commit();
        return {
             "success": True,
                        "message": "Users deleted successfully",
                        "userData": existingUser
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="failed to delete user data")





