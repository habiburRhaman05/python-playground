import enum
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import Mapped, relationship
from config.db import Base


# TYPE_CHECKING prevents circular import crashes at runtime
if TYPE_CHECKING:
    from .postModel import Post
    from .commentModel import Comment
    from .likeModel import Like

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=True, default=UserRole.USER)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
    likes: Mapped[List["Like"]] = relationship(
    "Like",
    back_populates="user"
)