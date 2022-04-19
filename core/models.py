from sqlalchemy import Column, String
from sqlalchemy.types import Date
from core.database import Base


class UserDetails(Base):
    __tablename__ = "user_details"

    username = Column(String(100), primary_key=True, index=True)
    email = Column(String(100))
    profile_img = Column(String(200))
    password = Column(String(200))
