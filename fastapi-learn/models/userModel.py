from sqlalchemy import  Column, Integer, String,select,delete,update
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()
class User (Base):
    __tablename__  = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=True)
    email = Column(String,nullable=True,unique=True)
    password = Column(String,nullable=False)
