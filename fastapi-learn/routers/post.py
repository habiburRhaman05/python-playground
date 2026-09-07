from fastapi import APIRouter,Depends,HTTPException
from typing import Annotated
from schema.postSchema import postPayload
from utils.security import oauth2_scheme
from sqlalchemy.orm import Session,joinedload,selectinload
from sqlalchemy import select,update,delete
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
    postStmt = select(Post).options(joinedload(Post.author), selectinload(Post.comments)).where(Post.id == id);
    existPost = db.execute(postStmt).scalar_one_or_none();
    if not existPost:
        raise HTTPException(detail="Invalid Post Id",status_code=404)
    print(existPost.author.id)
    postOwner = True if existPost.author.id == author.id else False
    if postOwner == False:
        raise HTTPException(detail="you dont have permisson to update this post",status_code=403)
    updatedData = payload.model_dump(exclude_unset=True);
    updatePostStmt = update(Post).where(Post.id == id).values(**updatedData)
    result = db.execute(updatePostStmt);
    if result.rowcount == 0 :
        raise HTTPException(detail="Failed to update post",status_code=400)
    db.commit()
    return {
        "message":"Post update successfully",
        "status_code":200
    }


@router.delete("/:id")
def createPost(id:int,author:User=Depends(requre_user),db:Session=Depends(get_db)):
    postStmt = select(Post).where(Post.id == id);
    existPost = db.execute(postStmt).scalar_one_or_none();
    if not existPost:
        raise HTTPException(detail="Invalid Post Id",status_code=404)
    print(existPost.author.id)
    postOwner = True if existPost.author.id == author.id else False
    if postOwner == False:
        raise HTTPException(detail="you dont have permisson to update this post",status_code=403)
    
    deletePostStmt = delete(Post).where(Post.id == id)
    result = db.execute(deletePostStmt);
    if result.rowcount == 0 :
        raise HTTPException(detail="Failed to update post",status_code=400)
    db.commit()
    return {
        "message":"Post deleted successfully",
        "status_code":200
    }



@router.get("/")
def createPost(author:User=Depends(requre_user),db:Session=Depends(get_db)):
    postsStmt = select(Post).options(joinedload(Post.author),selectinload(Post.comments)).where(Post.author_id == author.id)
    result = db.scalars(postsStmt).all()
    return {
        "message":"Post fetch successfully",
        "status_code":200,
        "posts":result
    }
