from distill.exceptions import HTTPErrorResponse, HTTPForbidden
from distill.request import Request
from brainstorm.sql import Session
from brainstorm.sql.orm import APIToken
from sqlalchemy.orm.collections import InstrumentedList


def il_json(il, request):
    return [i for i in il]

InstrumentedList.json = il_json


class RESTful(object):
    def __init__(self, methods=None):
        if not methods:
            methods = ["GET"]
        self.methods = methods

    def __call__(self, func):
        def check_method(*args, **kwargs):
            if isinstance(args[0], Request):
                req = args[0]
                res = args[1]
            else:
                req = args[1]
                res = args[2]

            res.headers['Access-Control-Allow-Origin'] = '*'  # TODO: Should be sane in production
            res.headers['Access-Control-Allow-Headers'] = 'Authorization'
            if req.env['REQUEST_METHOD'].upper() == 'OPTIONS':
                res.headers['Allow'] = ', '.join(self.methods)
                return res
            elif req.env['REQUEST_METHOD'].upper() not in self.methods:
                return HTTPErrorResponse("405 Method Not Allowed", None)
            return func(*args, **kwargs)
        return check_method


def auth_required(func):
    def _check_auth(*args, **kwargs):
        if isinstance(args[0], Request):
            req = args[0]
            res = args[1]
        else:
            req = args[1]
            res = args[2]
        if not req.user:
            return HTTPForbidden()
        return func(*args, **kwargs)
    return _check_auth


def check_auth(req, res):
    if 'authorization' in req.headers:
        token = Session().query(APIToken).filter(APIToken.token == req.headers['authorization']).scalar()
        req.user = token.user
    else:
        req.user = None