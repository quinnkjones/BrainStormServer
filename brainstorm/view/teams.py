__author__ = 'quinn'
from distill.exceptions import HTTPNotFound, HTTPInternalServerError, HTTPMoved
from distill.renderers import renderer

from brainstorm.sql import Teams, Session
from brainstorm.utils import RESTful, auth_required


class TeamController(object):
    @RESTful(['POST'])
    @auth_required
    @renderer('prettyjson')
    def create_new(self,request,response):
        userid = request.matchdict['userid']
        newTeam = Teams(userid,request.POST['name'])
        Session().add(newTeam)
        Session().commit()

        request.POST['data']
