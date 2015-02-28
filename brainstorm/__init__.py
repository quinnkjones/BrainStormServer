from distill.application import Distill


def main(**settings):
    app = Distill(settings=settings)

    return app
