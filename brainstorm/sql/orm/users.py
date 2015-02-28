from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, String, Integer

from brainstorm.sql import DecBase


class User(DecBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64))
    password = Column(String(256))