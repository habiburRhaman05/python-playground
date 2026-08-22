from sqlalchemy import create_engine, Column, Integer, String, select, delete, update
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from .env import envVariables 

# 1. FIX PROPERTY NAME: Change to match your Pydantic class property definition
db_engine = create_engine(envVariables.DATABASE_URL) 
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# 2. ADD THIS LINE: This gives Alembic and your Models the Base metadata anchor it needs!
Base = declarative_base()

def get_db():
    db = sessionLocal() 
    try:
        yield db        
    finally:
        db.close()
