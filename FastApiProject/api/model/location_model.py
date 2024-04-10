from sqlalchemy import Column, ForeignKey, func, Integer
from sqlalchemy.types import String, DateTime
# from sqlalchemy.orm import relationship
from .device_model import Device
from . import Base
from pydantic import BaseModel
from datetime import datetime

class LocationCreate(BaseModel):
    device_id: int
    location: str
    location_date: datetime


class Location(Base):
    __tablename__ = "Locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(ForeignKey(Device.id))
    location = Column(String)
    location_date = Column(DateTime)
    created_date = Column(DateTime, default=func.now())
