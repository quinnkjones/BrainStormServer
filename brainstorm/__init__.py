from distill.application import Distill
from distill.renderers import JSON
from brainstorm.sql import sql_init
from brainstorm.view import add_controllers, map_routes


def main(**settings):
    app = Distill(settings=settings)

    sql_init(settings['sql.dsn'])

    add_controllers(app)
    map_routes(app)

    app.add_renderer('prettyjson', JSON(indent=4))
    return app
