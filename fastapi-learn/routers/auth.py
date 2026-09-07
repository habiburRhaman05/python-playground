from pydantic import BaseModel,EmailStr
from fastapi import status,HTTPException,Depends,APIRouter,Response,Header
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select,update,delete
from sqlalchemy.exc import SQLAlchemyError
from config.db import get_db
from models.userModel import User
from utils.pwdlib import get_password_hash,verify_password
from schema.authSchema import UpdateSchema,registerPayload,registerResponse,loginPayload,LoginResponse,UserData
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
    # 1. Decode token
    userId = getToken(token)
    print(f"--- DEBUG: Extracted userId: {userId} ---")
    
    if not userId:
        raise HTTPException(status_code=401, detail="Invalid token session. Please login again.")
    # 2. Fetch User from Database safely
    try:
        user = getUserFromDB(db, userId) 
    except Exception as db_err:
        print(f"--- DATABASE CRASH inside getUserFromDB: {str(db_err)} ---")
        raise HTTPException(status_code=500, detail="Database lookup failed.")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 3. Format output data carefully to match your UserData schema
    print(f"--- DEBUG: Found database user: {user.email} (ID: {user.id}) ---")
    
    try:
        return {
            "id": user.id,          # Check if your UserData schema calls this 'id' or something else
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "token": token
        }
    except Exception as validation_err:
        print(f"--- PYDANTIC VALIDATION CRASH: {str(validation_err)} ---")
        raise HTTPException(
            status_code=500, 
            detail=f"Schema parsing error: Ensure dictionary keys match your UserData model fields."
        )

def requre_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    userId = getToken(token)

    if not userId:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = getUserFromDB(db, userId)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user

# admin routes
@router.get("/users")
def allUsers(
    user=Depends(requre_admin),db:Session=Depends(get_db)
):
    getAllQuery = select(User)
    allUsers = db.scalars(getAllQuery).all()
    return allUsers

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
           "sub":str(userExist.id),
           "email":userExist.email,
           "name":userExist.name,
           "role":userExist.role
       }

       access_token = create_access_token(data=tokenPayload)
       response.set_cookie("token",value=access_token,httponly=True,samesite='lax',max_age=60*30,secure=True)
       return {
        "message": "Login successful",
            "statusCode": 200,
            "access_token": access_token, 
            "token_type": "bearer", 
            "userData": {
                "id": userExist.id,
                "email": userExist.email,
                "name": userExist.name,
                "role": userExist.role,
                "token": access_token
            }
       }
    except SQLAlchemyError as e:
        raise HTTPException(
        status_code=500, 
        detail="A database error occurred while processing your request. Failed to login"
        )




@router.put("/me:/id/update")
async def updateProfile(id:int,payload:UpdateSchema,db:Session=Depends(get_db)):
    updateData = payload.model_dump(exclude_unset=True);
    if not updateData:
        raise HTTPException(details="no field found") 
    updateQuery = update(User).where(User.id == id).values(**updateData);
    result = db.execute(updateQuery)
    if result.rowcount == 0:
        raise HTTPException(detail="failed to update profile",status_code=500)
    db.commit();
    return {"message":"Profile updated successfully"}
    

@router.delete("/me:/id/update")
def deleteUser(id:int,user =Depends(requre_admin),db:Session=Depends(get_db)):
    deleteUser = delete(User).where(User.id == id)
    result = db.execute(deleteUser);
    if result.rowcount == 0 :
        raise HTTPException(detail="failed to delete profile",status_code=500)
    db.commit()
    return {"message":"user delated successfully"}

