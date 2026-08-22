from fastapi import FastAPI, status, HTTPException, Depends
from config.db import Base, db_engine  # ১. প্রথমে বেস ও ইঞ্জিন ইমপোর্ট করুন

# ২. রুটারগুলো ইমপোর্ট করুন (রুটার ইমপোর্ট হলে এর ভেতরের UserModel-ও পাইথনে রেজিস্টার্ড হয়ে যাবে)
from routers.books import router as books_router
from routers.user import router as userRouter
from routers.auth import router as authRouter

# ৩. রুটার (এবং মডেল) ইমপোর্ট হওয়ার পর টেবিল ক্রিয়েশন কমান্ড রান করুন
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
