from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id = Column(Integer, ForeignKey('animes.id'))
    status = Column(String)
    user = relationship("UserDB", back_populates="history_items")
    anime = relationship("AnimeDB")