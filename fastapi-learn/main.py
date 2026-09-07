from fastapi import FastAPI, status, HTTPException, Depends
from config.db import Base, db_engine 
from routers.auth import router as authRouter
from routers.post import router as postRouter
from fastapi.security import OAuth2PasswordBearer
# In your main app startup file (e.g., main.py)
from models.userModel import User
from models.postModel import Post
from models.commentModel import Comment
from models.likeModel import Like  # 👈 Add this line (adjust path if your file name is different)

Base.metadata.create_all(bind=db_engine)

app = FastAPI(
    title="fast api project"
)

app.include_router(authRouter)
app.include_router(postRouter)

@app.get("/")
def read_root():
    return {"message": "Hello World Fasstapi"}
