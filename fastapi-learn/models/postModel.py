from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base

if TYPE_CHECKING:
    from .userModel import User
    from .commentModel import Comment
    from .likeModel import Like


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    title: Mapped[str] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)
    thumbnail: Mapped[str] = mapped_column(nullable=False)

    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post"
    )

    likes: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="post"
    )