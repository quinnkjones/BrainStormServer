from sqlalchemy.orm import backref, relationship
from sqlalchemy import Table,Column, String, Integer, ForeignKey, PrimaryKeyConstraint

from brainstorm.sql import DecBase


userteams = Table('userteams',DecBase.metadata,
                  Column('userid',Integer,ForeignKey('user.id')),
                  Column('teamid',Integer,ForeignKey('team.id')))

class User(DecBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64))
    password = Column(String(256))
    email = Column(String(128))
    teams = relationship("team",secondary = userteams)

    def __init__(self,name,password,email):
        self.username = name
        self.password = password
        self.email = email

    def json(self, request):
        return {
            "username": self.username,
            "gravatar": self.email,
            "speciality":self.speciality
        }


class Teams(DecBase):
    __tablename__ = "teams"

    id = Column(Integer,primary_key = True,autoincrement=True)
    owner = Column(Integer,ForeignKey('user.id'))
    name = Column(String(64))
    users = relationship("user",secondary = userteams)

    def __init__(self,owner,name):
        self.name = name
        self.owner = owner

    def json(self,request):
        return {
            "name":self.name,
            "owner":self.owner.username,
            "users":[request.url("user",userid = x.id) for x in self.users]
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





