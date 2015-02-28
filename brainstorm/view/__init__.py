from distill.exceptions import HTTPNotFound, HTTPForbidden


def add_controllers(app_):
    from .ideas import IdeaController

    loc = locals().copy()
    del loc['app_']
    [app_.add_controller(name.lower(), obj) for name, obj in loc.items()]