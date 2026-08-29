from utils.jwt_utils import verify_access_token
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import User
from fastapi import HTTPException

def getUserFromDB(id:int,db:Session):
    try :
         user = db.query(User).filter(User.id == id).first();
         if not user:
          raise HTTPException(detail="user not found")
         return {
        "name":user.name,
        "email":user.email,
        "role":user.role,
        "id":user.id
        }

    except SQLAlchemyError as e:
            raise HTTPException(detail="failed to get user")




def getToken(token: str) -> int | None:
    # 👈 খুবই গুরুত্বপূর্ণ চেক: যদি টোকেনের শুরুতে 'Bearer ' লেখা থাকে, তা কেটে শুধু আসল টোকেনটুকু নিন
    print(token)
  
    verifyToken = verify_access_token(token)
    print(verifyToken)
    if not verifyToken or "sub" not in verifyToken:
        return None
        
    return int(verifyToken["sub"])

     

