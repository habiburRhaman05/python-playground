from fastapi import FastAPI, status, HTTPException, Depends
from config.db import Base, db_engine 

from routers.books import router as books_router
from routers.user import router as userRouter
from routers.auth import router as authRouter
from fastapi.security import OAuth2PasswordBearer

Base.metadata.create_all(bind=db_engine)

app = FastAPI(
    title="fast api project"
)


app.include_router(books_router)
app.include_router(userRouter)
app.include_router(authRouter)

@app.get("/")
def read_root():
    return {"message": "Hello World Fasstapi"}
