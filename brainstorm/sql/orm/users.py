import hashlib
from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint

from brainstorm.sql import DecBase


class User(DecBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64))
    password = Column(String(256))
    gravatar = Column(String(128))
    speciality = Column(String(64))

    def json(self, request):
        return {
            "username": self.username,
            "gravatar": "//gravatar.com/avatar/%s" % hashlib.md5(bytes(self.gravatar, 'utf-8')).hexdigest(),
            "speciality":self.speciality
        }


class APIToken(DecBase):
    __tablename__ = "tokens"

    userid = Column(Integer, ForeignKey('users.id'))
    token = Column(String(256))
    user = relationship('User', backref='tokens')

    __table_args__ = (PrimaryKeyConstraint('userid', 'token'),)

    def __init__(self, userid, token):
        self.userid = userid
        self.token = token
