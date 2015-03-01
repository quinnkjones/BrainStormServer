import os
from distill.exceptions import HTTPNotFound, HTTPUnauthorized, HTTPInternalServerError
from distill.renderers import renderer
import sys
from brainstorm.sql import User, Session, APIToken
from brainstorm.utils import RESTful
from passlib.hash import pbkdf2_sha512
import hashlib


class APIController(object):
    @RESTful()
    @renderer('prettyjson')
    def get_base(self, request, response):
        return {
            "login": request.url('login', qualified=True),
            "ideas": request.url('idea_list', qualified=True),
            "media": request.url('media_list', qualified=True)
        }

    @RESTful(['GET', 'POST'])
    @renderer('prettyjson')
    def login(self, request, response):
        if 'username' in request.POST:
            user = Session().query(User).filter(User.username == request.POST['username']).scalar()
            if not user:
                return HTTPNotFound()

            if pbkdf2_sha512.verify(request.POST['password'], user.password):
                token = hashlib.sha512(os.urandom(32)).hexdigest()
                Session().add(APIToken(user.id, token))
                try:
                    Session().commit()
                except:
                    print(sys.exc_info())
                    Session().rollback()
                    return HTTPInternalServerError()
                return {"token": token}
        return HTTPUnauthorized()