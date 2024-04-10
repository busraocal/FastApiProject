from sqlalchemy import Column, func
from sqlalchemy.types import String, Integer, DateTime, JSON
from . import Base


class Log(Base):
    __tablename__ = "Logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String)
    data = Column(String)
    created_date = Column(DateTime, default=func.now())
