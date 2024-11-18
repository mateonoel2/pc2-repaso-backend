from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from .user import user_favorites

class AnimeDB(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    users_favorited = relationship(
        "UserDB",
        secondary=user_favorites,
        back_populates="favorites"
    )