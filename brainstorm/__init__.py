from distill import Distill


def main(**settings):
    app = Distill(settings=settings)

    return app
