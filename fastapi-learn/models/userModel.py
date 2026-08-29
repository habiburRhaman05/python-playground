from sqlalchemy import Column, Integer, String,Enum
import enum
from config.db import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole),nullable=True,default=UserRole.USER)