from distill.exceptions import HTTPInternalServerError, HTTPNotFound
from distill.renderers import renderer
from brainstorm.sql import Comment, Session
from brainstorm.utils import RESTful, auth_required


class FeedbackController(object):
    @RESTful(['GET', 'POST'])
    @auth_required
    @renderer('prettyjson')
    def comments(self, request, response):
        if request.env['REQUEST_METHOD'].upper() == 'POST':
            comment = Comment(request.user.id, int(request.POST['idea']), request.POST['message'])
            Session().add(comment)
            try:
                Session().commit()
            except:
                Session().rollback()
                raise HTTPInternalServerError()

        return [request.url('get_comment', cid=i.id, qualified=True) for i in request.user.comments]

    @RESTful(['GET', 'POST', 'PUT', 'DELETE'])
    @auth_required
    @renderer('prettyjson')
    def comment(self, request, response):
        comment = Session().query(Comment).filter(Comment.id == int(request.matchdict['cid'])).scalar()
        if not comment:
            raise HTTPNotFound()
        return comment