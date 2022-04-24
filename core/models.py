from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import Date, Text
from core.database import Base


class UserDetails(Base):
    __tablename__ = "user_details"
    username = Column(String(100), primary_key=True, index=True)
    email = Column(String(100))
    profile_img = Column(String(200))
    password = Column(String(200))

class Tasks(Base):
    __tablename__ = "user_tasks"
    task_id = Column(String(50), primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text(500))
    assigned_to = Column(String(100), ForeignKey("user_details.username"))
    status = Column(Integer, default=0)