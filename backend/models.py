from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime


class Flat(Base):
    __tablename__ = 'flat'

    id = Column(Integer, primary_key=True)
    rooms = Column(Integer, default=None)
    price = Column(Float, nullable=False)
    area = Column(Float, nullable=False)
    permalink = Column(String(50), nullable=False)
    published = Column(DateTime, default=datetime.utcnow())
