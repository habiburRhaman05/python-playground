from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends,APIRouter,Response,Header
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from config.db import get_db
from models.userModel import User
from utils.pwdlib import get_password_hash,verify_password
from schema.authSchema import registerPayload,registerResponse,loginPayload,LoginResponse,UserData
from utils.jwt_utils import create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import oauth2_scheme  
from utils.auth_utils import getToken,getUserFromDB
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)



@router.get("/me", response_model=UserData, status_code=status.HTTP_200_OK)
def getUserData(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    userId = getToken(token)
    print(userId)
    # সেফটি চেক: টোকেন রিড করতে না পারলে সরাসরি ৪০১ এরর দিন
    if not userId:
        raise HTTPException(status_code=401, detail="Invalid token session. Please login again.")
        
    #  সঠিক অর্ডার: প্রথম প্যারামিটারে db সেশন পাস করুন
    user = getUserFromDB(db, userId) 
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "token": token
    }


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
            password=hashPassword,
            role=payload.role
        )
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return {
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



@router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def loginUser( response:Response, userInfo:OAuth2PasswordRequestForm = Depends() ,db: Session=Depends(get_db)):
    try:
       userExistQuery = select(User).where(User.email == userInfo.username)
       userExist = db.execute(userExistQuery).scalar_one_or_none()
       if not userExist:
           raise HTTPException(detail="user not found",status_code=status.HTTP_404_NOT_FOUND)
       passwordMatch = verify_password( userInfo.password, userExist.password);
       if not passwordMatch:
           raise HTTPException(detail="Password not match",status_code=status.HTTP_400_BAD_REQUEST);
       tokenPayload = {
           "sub":userExist.id,
           "email":userExist.email,
           "name":userExist.name,
           "role":userExist.role
       }

       token = create_access_token(tokenPayload,timedelta(minutes=30));
       response.set_cookie("token",value=token,httponly=True,samesite='lax',max_age=60*30,secure=True)
       return {
        "message": "Login successful",
            "statusCode": 200,
            "access_token": token,  # 👈 মূল টোকেনটি এখানেও পাঠাতে হবে
            "token_type": "bearer",  # 👈 এটিও থাকতে হবে
            "userData": {
                "id": userExist.id,
                "email": userExist.email,
                "name": userExist.name,
                "role": userExist.role,
                "token": token
            }
       }
    except SQLAlchemyError as e:
        raise HTTPException(
        status_code=500, 
        detail="A database error occurred while processing your request. Failed to login"
        )



