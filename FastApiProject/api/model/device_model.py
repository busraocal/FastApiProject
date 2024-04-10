from sqlalchemy import Column, func
from sqlalchemy.types import String, Integer, DateTime
from . import Base
from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str


class Device(Base):
    __tablename__ = "Devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created_date = Column(DateTime, default=func.now())
