from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from brainstorm.sql import DecBase


class Idea(DecBase):
    __tablename__ = "idea"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    desc = Column(String(1024))
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='ideas')

    def __init__(self, title, description, userid, progress=0):
        self.title = title
        self.desc = description
        self.userid = userid
        self.progress = progress


class Media(DecBase):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)
    value = Column(String(1024))
    ideaid = Column(Integer, ForeignKey('ideas.id'))
    idea = relationship('Idea', backref='media')

    def _init__(self, type, value, ideaid):
        self.type = type
        self.value = value
        self.ideaid = self.ideaid


class Transcription(DecBase):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mediaid = Column(Integer, ForeignKey('media.id'))
    media = relationship('Media', backref=backref('transcription', uselist=False))
    transcription = Column(String(256))

    def __init__(self, media, transcription):
        self.mediaid = media
        self.transcription = transcription