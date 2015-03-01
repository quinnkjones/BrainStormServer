from distill.exceptions import HTTPNotFound, HTTPInternalServerError
from distill.renderers import renderer
from brainstorm.sql import Comment, Session
from brainstorm.utils import RESTful, auth_required


class FeedbackController(object):
    @RESTful(['GET', 'POST'])
    @auth_required
    @renderer('prettyjson')
    def comments(self, request, response):
        print("Got there")
        if request.env['REQUEST_METHOD'].upper() == 'POST':
            comment = Comment(request.user.id, int(request.POST['idea']), request.POST['message'])
            Session().add(comment)
            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()

        return [request.url('get_comment', cid=i.id, qualified=True) for i in request.user.comments]