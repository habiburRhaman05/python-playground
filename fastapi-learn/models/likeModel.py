from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base


if TYPE_CHECKING:
    from .postModel import Post
    from .userModel import User


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="likes"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="likes"
    )