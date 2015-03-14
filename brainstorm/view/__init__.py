import mimetypes
import os
from distill.exceptions import HTTPNotFound, HTTPForbidden
from brainstorm.utils import auth_required


def add_controllers(app_):
    from .ideas import IdeaController, MediaController, TransController
    from .teams import TeamController
    from .apibase import APIController
    from .feedback import FeedbackController
    from .home import FrontController

    loc = locals().copy()
    del loc['app_']
    [app_.add_controller(name.lower(), obj) for name, obj in loc.items()]


def map_routes(app):
    app.map_connect('home', '/', controller='frontcontroller', action='home')
    app.map_connect('api_base', '/api', controller='apicontroller', action='get_base')
    app.map_connect('get_ideas', '/api/ideas', controller='ideacontroller', action='ideas')
    app.map_connect('get_idea', '/api/ideas/{ideaid}', controller='ideacontroller', action='idea')
    app.map_connect('get_comments', '/api/comments', controller='feedbackcontroller', action='comments')
    app.map_connect('get_comment', '/api/comments/{cid}', controller='feedbackcontroller', action='comment')
    app.map_connect('media_list', '/api/media', controller='mediacontroller', action='get_media_list')
    app.map_connect('media_obj', '/api/media/{mid}', controller='mediacontroller', action='get_media')
    app.map_connect('get_transcription','/api/trans/{tid}',controller = 'transcontroller',action = 'get_transcription')
    # app.map_connect('focus_connect','/api/ideas/{ideaid}/connect',controller='ideacontroller',action='make_connections')
    app.map_connect('login', '/api/auth', controller='apicontroller', action='login')
    app.map_connect('user', '/api/user/{userid}', controller='apicontroller', action='get_user')
    app.map_connect('new_team','/api/user/{userid}/team',controller='teamcontroller', action='create_new')
    app.map_connect('static', '/static/{pathspec:.+}', action=static)


@auth_required
def static(request, response):
    path = os.path.join(request.settings['staticdir'], request.matchdict['pathspec'])
    if os.path.isfile(path):
        t = mimetypes.guess_type(request.matchdict['pathspec'])
        if t[0]:
            response.headers['Content-Type'] = t[0]
        response.headers['Cache-Control'] = 'max-age=3600'
        # response.headers['X-Content-Type-Options'] = 'nosniff'
        response.file = open(path, 'rb')
        response.file_len = os.path.getsize(path)
