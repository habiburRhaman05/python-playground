from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.userModel import User  # Ensure this matches your import path exactly
from fastapi import HTTPException, status
from utils.jwt_utils import verify_access_token

def getUserFromDB(db: Session, id: int):
 
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return user  # Return the object model directly so 'user.email' works in the router
        
    except SQLAlchemyError as e:
        print(f"Database error in getUserFromDB: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to get user from database"
        )

def getToken(token: str):
    payload = verify_access_token(token)
    print("DEBUG payload:", payload)
    if payload is None:
        return None
    return payload.get("sub")  # Extracting 'sub' claim which holds your user ID
