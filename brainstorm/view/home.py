from distill.renderers import renderer


class FrontController(object):
    @renderer('app.mako')
    def home(self, request, response):
        return {}