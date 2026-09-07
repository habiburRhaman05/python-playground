from fastapi import APIRouter,Depends,HTTPException
from typing import Annotated
from schema.postSchema import postPayload
from utils.security import oauth2_scheme
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import get_db
from utils.auth_utils import getToken,getUserFromDB
from schema.userSchema import User
from models.postModel import Post
router = APIRouter(
    prefix="/post",
    tags=["post"]
)

def requre_user(
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

    if user.role != "user":
        raise HTTPException(
            status_code=403,
            detail="user access required"
        )
    return user


@router.post("/")
def createPost(payload:postPayload,author:User=Depends(requre_user),db:Session=Depends(get_db)):
    newPost =  Post(
        title = payload.title,
        content = payload.content,
        thumbnail = payload.thumbnail,
        author_id = author.id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return {
        "message":"Post creation successfully",
        "status_code":200
    }
    


@router.put("/:id")
def createPost(id:int,payload:postPayload,author:User=Depends(requre_user),db:Session=Depends(get_db)):
    postStmt = select(Post).where(Post.id == id);
    existPost = db.execute(postStmt).scalar_one_or_none();
    if not existPost:
        raise HTTPException(detail="Invalid Post Id",status_code=404)
    print(existPost)
    return {
        "message":"Post update successfully",
        "status_code":200
    }
    