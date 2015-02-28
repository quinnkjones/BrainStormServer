from distill.application import Distill
from distill.renderers import JSON
from brainstorm.sql import sql_init


def main(**settings):
    app = Distill(settings=settings)

    sql_init(settings['sql_dsn'])

    app.add_renderer('prettyjson', JSON(indent=4))
    return app
