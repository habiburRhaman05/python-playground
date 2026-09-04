from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import INTEGER, ForeignKey
from typing import List,TYPE_CHECKING
from config.db import Base


if TYPE_CHECKING :
    from models.postModel import Post 

class Like(Base):
    __tablename__ = "likes"
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    count: Mapped[int] = mapped_column(INTEGER, default=0)
    
    # Assuming a Like belongs to a specific Post
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="likes")
