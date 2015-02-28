from distill.renderers import renderer


class IdeaController(object):
    @renderer('prettyjson')
    def get_ideas(self, request, resposne):
        return request.user.ideas
