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
from utils.exceptions import UserNotFoundError,DuplicateEmailError,AppBaseException
from fastapi import Request,status
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=db_engine)

app = FastAPI(
    title="fast api project"
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter)
app.include_router(postRouter)



# 1. Catch specific business logic errors
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "error_type": "NOT_FOUND", "detail": exc.message}
    )

@app.exception_handler(DuplicateEmailError)
async def duplicate_email_handler(request: Request, exc: DuplicateEmailError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"success": False, "error_type": "ALREADY_EXISTS", "detail": exc.message}
    )

# 2. Catch all unexpected database or system crashes (Fallback safety net)
@app.exception_handler(Exception)
async def global_crash_handler(request: Request, exc: Exception):
    # In production, log 'exc' here to Sentry or a log file for debugging
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "error_type": "INTERNAL_SERVER_ERROR", "detail": "Something went wrong internally."}
    )

@app.get("/")
def read_root():
    return {"message": "Hello World Fasstapi"}
@app.get("/health")
def read_root():
    return {"health":"ok"}
