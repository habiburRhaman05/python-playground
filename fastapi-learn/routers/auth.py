from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config.db import get_db
from models.userModel import User
from utils.pwdlib import get_password_hash,verify_password
from schema.authSchema import registerPayload,registerResponse,loginPayload,loginResponse


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post("/register",response_model=registerResponse,status_code=status.HTTP_201_CREATED)
def registerUser(payload:registerPayload,db:Session=Depends(get_db)):
    try:
        existQuery = select(User).where(User.email == payload.email)
        existingUser = db.execute(existQuery).scalar_one_or_none()
        if existingUser :
            raise HTTPException(status_code=402,detail="this email already used - try another one")

        hashPassword = get_password_hash(payload.password)
        newUser = User(
            name=payload.name,
            email=payload.email,
            password=hashPassword
        )
        db.add(newUser)
        db.commit()
        db.refresh()
        return {
            "userData":newUser,
            "message":"register successsfully",
            "statusCode":status.HTTP_201_CREATED
        }
    except SQLAlchemyError as db_err:
        # CRITICAL: Roll back changes so your database connection isn't left hanging in an error state
        db.rollback() 
        
        # Log the actual mechanical error to your terminal for development debugging
        print(f"Database insertion failed: {str(db_err)}") 
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while creating your account. Please try again."
        )
        
    except Exception as e:
        db.rollback()
        print(f"Unexpected system error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed due to invalid inputs or system constraints."
        )

