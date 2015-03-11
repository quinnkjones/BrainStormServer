import os
from distill.exceptions import HTTPNotFound, HTTPInternalServerError, HTTPMoved
from distill.renderers import renderer
import shutil
from brainstorm.sql import Idea, Session, Media, Transcription
from brainstorm.utils import RESTful, auth_required
import speech_recognition as sr
from threading import Thread
import subprocess
import logging


def recognize(sourceFile, mid):
    r = sr.Recognizer()
    with sr.WavFile(sourceFile) as source:
        audio = r.record(source)  # extract audio data from the file
        logging.basicConfig(filename = './example.log',level=logging.DEBUG)
        try:
            list = r.recognize(audio, True)
            logging.debug('finished transcription'+ list[0]["text"])# generate a list of possible transcriptions
            t = Transcription(mid, list[0]["text"])
            Session().add(t)


            try:
                Session().commit()
            except:
                Session().rollback()
                logging.exception('Session had to rollback on transcription')


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

            logging.basicConfig(filename='./example.log',level=logging.DEBUG)

            idea = Idea(request.user.id)
            Session().add(idea)
            Session().commit()
            media = Media(2,idea.id ,request.user.id)
            Session().add(media)
            Session().commit()

            ext = request.POST['ext']



            if ext !='wav':
                path1 = os.path.join('media',str(media.id)+'.'+ext)
                source = os.path.join(request.settings['staticdir'],path1)
                fid = open(os.path.join(request.settings['staticdir'],path1),'wb')
                shutil.copyfileobj(request.POST['value'].file,fid)
                fid.close()
                path = os.path.join('media', '%i.wav' % media.id)
                dest = os.path.join(request.settings['staticdir'], path)
                ret = subprocess.call(['avconv','-i',source,dest])
                ret = subprocess.call(['rm',source])
            else:
                path = os.path.join('media', '%i.wav' % media.id)
                fid = open(os.path.join(request.settings['staticdir'], path), 'wb')
                shutil.copyfileobj(request.POST['value'].file, fid)
                fid.close()


            media.value = path

            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()
            p = Thread(target = recognize, args = (os.path.join(request.settings['staticdir'],path),media.id,))
            p.start()
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

    # @RESTful(['GET','POST'])
    # @auth_required
    # @renderer('prettyjson')
    # def focus_connect(self,request,response):
    #     if request.env['REQUEST_METHOD'].upper() == 'GET':
    #         idea = Session().query(Idea).filter(Idea.id == int(request.matchdict['ideaid'])).scalar()
    #         f = idea.focusarea
    #         users = Session.query(User).filter(User.speciality == f).all()
    #         return users if not users is None else []
    #     elif request.env['REQUEST_METHOD'].upper() == 'POST':
    #         focus = request.POST['focus']
    #         idea = Session().query(Idea).filter(Idea.id == int(request.matchdict['ideaid'])).scalar()
    #         idea.focusarea = focus
    #         Session.commit()
            


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

class TransController(object):
    @RESTful(['GET'])
    @auth_required
    @renderer('prettyjson')
    def get_transcription(self,request,response):
        transID = request.matchdict['tid']
        logging.basicConfig(filename='./example.log',level=logging.DEBUG)
        logging.debug(str(transID))
        transc = Session().query(Transcription).filter(Transcription.id == int(transID)).scalar()
        logging.debug(str(transc))
        if not transc:
            raise HTTPNotFound()
        return transc
