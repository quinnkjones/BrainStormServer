from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from brainstorm.sql import DecBase
import time


class Idea(DecBase):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='ideas')
    timestamp = Column(Integer)

    def __init__(self, userid, progress=0, timestamp=None):

        self.userid = userid
        self.progress = progress
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = round(time.time())

    def json(self, request):
        return {
            "id": self.id,
            "user": request.url('user', userid=self.userid, qualified=True),
            "media": [request.url('media_obj', mid=i.id, qualified=True) for i in self.media],
            "transcription": request.url('get_transcription', tid=self.media[0].transcription.id, qualified=True) if
            self.media[0].transcription else [],
            "comments": [request.url('get_comment', cid=i.id, qualified=True) for i in self.comments],
            "likes": 0
        }


class Media(DecBase):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)
    value = Column(String(1024))
    ideaid = Column(Integer, ForeignKey('ideas.id'))
    idea = relationship('Idea', backref='media')
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='media')

    def __init__(self, type, ideaid, userid, value=None):
        self.type = type
        self.value = value
        self.ideaid = ideaid
        self.userid = userid

    def json(self, request):
        return {
            "id": self.id,
            "type": self.type,
            "transcription": request.url('get_transcription', tid=self.transcription.id,
                                         qualified=True) if self.transcription else None,
            "value": self.value if self.type == 1 else request.url('static', pathspec=self.value, qualified=True)
        }


class Transcription(DecBase):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mediaid = Column(Integer, ForeignKey('media.id'))
    media = relationship('Media', backref=backref('transcription', uselist=False))
    transcription = Column(String(500))

    def __init__(self, media, transcription):
        self.mediaid = media
        self.transcription = transcription

    def json(self, request):
        return {
            "value": self.transcription
        }