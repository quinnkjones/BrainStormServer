import os
from distill.exceptions import HTTPNotFound, HTTPInternalServerError, HTTPMoved
from distill.renderers import renderer
import shutil
from brainstorm.sql import Idea, Session, Media, Transcription
from brainstorm.utils import RESTful, auth_required
import speech_recognition as sr

import logging


def recognize(sourceFile, mid):
    r = sr.Recognizer()
    with sr.WavFile(sourceFile) as source:
        audio = r.record(source)  # extract audio data from the file
        logging.basicConfig(filename='/home/quinn/example.log',level=logging.DEBUG)
        try:
            list = r.recognize(audio, True)  # generate a list of possible transcriptions
            Session().add(Transcription(mid, list[0]["text"]))
            try:
                Session().commit()
            except:
                Session().rollback()

        except LookupError:
            print("Whoops")


class IdeaController(object):
    @RESTful(['GET', 'POST'])
    @auth_required
    @renderer('prettyjson')
    def ideas(self, request, response):
        if request.env['REQUEST_METHOD'].upper() == 'GET':
            return [request.url('get_idea', ideaid=i.id, qualified=True) for i in request.user.ideas]
        elif request.env['REQUEST_METHOD'].upper() == 'POST':
            desc = request.POST['desc']
            title = request.POST['title']
            idea = Idea(title, desc, request.user.id)
            Session().add(idea)
            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()
            raise HTTPMoved(location=request.url('get_idea', ideaid=idea.id))

    @RESTful(['GET', 'PUT', 'POST', 'DELETE'])
    @auth_required
    @renderer('prettyjson')
    def idea(self, request, response):
        if request.env['REQUEST_METHOD'].upper() == 'GET':
            idea = Session().query(Idea).filter(Idea.id == int(request.matchdict['ideaid'])).scalar()
            if not idea:
                raise HTTPNotFound()
            return idea

    @RESTful(['GET','POST'])
    @auth_required
    @renderer('prettyjson')
    def focus_connect(self,request,response):
        if request.env['REQUEST_METHOD'].upper() == 'GET':
            idea = Session().query(Idea).filter(Idea.id == int(request.matchdict['ideaid'])).scalar()
            f = idea.focusarea
            users = Session.query(User).filter(User.speciality == f).all()
            return users if not users is None else []
        elif request.env['REQUEST_METHOD'].upper() == 'POST':
            focus = request.POST['focus']
            idea = Session().query(Idea).filter(Idea.id == int(request.matchdict['ideaid'])).scalar()
            idea.focusarea = focus
            Session.commit()
            


class MediaController(object):
    @RESTful(['GET', 'POST'])
    @auth_required
    @renderer('prettyjson')
    def get_media_list(self, request, response):   
        
        if request.env['REQUEST_METHOD'].upper() == 'POST':
            ideaid = int(request.POST['idea'])
            type_ = int(request.POST['type'])
            media = Media(type_, ideaid, request.user.id)
            Session().add(media)
            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()
            if type_ == 1:
                value = request.POST['value']
                media.value = value
            elif type_ == 2:
                path = os.path.join('media', '%i.wav' % media.id)
                fid = open(os.path.join(request.settings['staticdir'], path), 'wb')
                shutil.copyfileobj(request.POST['value'].file, fid)
                fid.close()
                recognize(os.path.join(request.settings['staticdir'],path),media.id)
                media.value = path
            elif type_ == 3:
                path = os.path.join('media', '%i.mp4' % media.id)
                fid = open(os.path.join(request.settings['staticdir'], path), 'wb')
                shutil.copyfileobj(request.POST['value'].file, fid)
                media.value = path
                fid.close()
            elif type_ == 4:
                path = os.path.join('media', '%i.jpg' % media.id)
                fid = open(os.path.join(request.settings['staticdir'], path), 'wb')
                shutil.copyfileobj(request.POST['value'].file, fid)
                media.value = path
                fid.close()
            elif type_ == 5:
                path = os.path.join('media', '%i' % media.id)
                fid = open(os.path.join(request.settings['staticdir'], path), 'wb')
                shutil.copyfileobj(request.POST['value'].file, fid)
                media.value = path
                fid.close()
            Session().add(media)
            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()
            raise HTTPMoved(location=request.url('media_obj', mid=media.id))
        return [request.url('media_obj', mid=i.id, qualified=True) for i in request.user.media]

    @RESTful(['GET', 'POST'])
    @auth_required
    @renderer('prettyjson')
    def get_media(self, request, response):
        media = Session().query(Media).filter(Media.id == int(request.matchdict['mid'])).scalar()
        if not media:
            raise HTTPNotFound()
        return media
