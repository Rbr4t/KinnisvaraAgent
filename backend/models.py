from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Flat(Base):
    __tablename__ = 'flat'

    id = Column(Integer, primary_key=True)
    rooms = Column(Integer, default=None)
    price = Column(Float)
    area = Column(Float)
    permalink = Column(String(50), nullable=False)
    published = Column(DateTime, default=datetime.utcnow())
    location = Column(String(250))


class Search(Base):
    __tablename__ = 'user_searches'
    id = Column(Integer, primary_key=True)
    location = Column(String(250), nullable=False)
    price = Column(Float)
    area = Column(Float)
    rooms = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_parool = Column(String, nullable=False)

    piletid = relationship("Search", backref="users")


class User_Flats(Base):
    __tablename__ = "users_flats"

    id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey('flat.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
