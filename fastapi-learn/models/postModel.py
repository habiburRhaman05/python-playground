from typing import List, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from config.db import Base

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
