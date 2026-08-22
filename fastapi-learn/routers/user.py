from models.userModel import User
from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.exc import SQLAlchemyError
from schema.userSchema import userCreate,usercreateRes,allUsers,updateUserPayload
from sqlalchemy import select,delete
from sqlalchemy.orm import Session
from config.db import get_db
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",response_model=usercreateRes,status_code=status.HTTP_201_CREATED)
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

@router.get(
    "/",
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

@router.patch("/{id}",response_model=usercreateRes,status_code=status.HTTP_200_OK)
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

@router.delete("/{id}",response_model=usercreateRes,status_code=status.HTTP_200_OK)
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

