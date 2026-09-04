import enum
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import Mapped, relationship
from config.db import Base

# TYPE_CHECKING prevents circular import crashes at runtime
if TYPE_CHECKING:
    from .postModel import Post
    from .commentModel import Comment

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
    role = Column(Enum(UserRole), nullable=True, default=UserRole.USER)

    # Use string names for relationships; SQLAlchemy finds them in Base.metadata
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
