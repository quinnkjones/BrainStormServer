from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from brainstorm.sql import DecBase


class Comment(DecBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ideaid = Column(Integer, ForeignKey('ideas.id'))
    idea = relationship('Idea', backref='comments')
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='comments')
    message = Column(String(1024))

    def __init__(self, user, idea, message):
        self.userid = user
        self.ideaid = idea
        self.message = message

    def json(self, request):
        return {
            "idea": request.url('get_idea', ideaid=self.ideaid),
            "user": self.user.json(request),
            "message": self.message
        }


class Commit(DecBase):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ideaid = Column(Integer, ForeignKey('ideas.id'))
    idea = relationship('Idea', backref='commits')
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='commits')
    message = Column(String(1024))
    progress = Column(Integer)

    def __init__(self, user, idea, message, progress):
        self.userid = user
        self.ideaid = idea
        self.message = message
        self.progress = progress
