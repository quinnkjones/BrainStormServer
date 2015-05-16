__author__ = 'quinn'
from distill.exceptions import HTTPNotFound, HTTPInternalServerError, HTTPMoved
from distill.renderers import renderer


from brainstorm.sql import Teams, User, Session
from brainstorm.utils import RESTful, auth_required


class TeamController(object):
    @RESTful(['POST'])
    @auth_required
    @renderer('prettyjson')
    def create_new(self,request,response):
        userid = int(request.matchdict['userid'])
        newTeam = Teams(Session().query(User).filter(User.id == userid).one(),request.POST['name'])
        Session().add(newTeam)
        Session().commit()

        #TODO assume for now that users in group will be identified by idnum, reevaluate if names are easier for will

        users = request.POST['data']

        for u in users.split(','):
            newTeam.users.append(Session().query(User).filter(User.id == int(u)).one())

        return newTeam.id
