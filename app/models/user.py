from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


user_favorites = Table(
    'user_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('anime_id', Integer, ForeignKey('animes.id'))
)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    favorites = relationship(
        "AnimeDB",
        secondary=user_favorites,
        back_populates="users_favorited"
    )
    history_items = relationship("UserHistory", back_populates="user")