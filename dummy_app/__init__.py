from pyramid.config import Configurator
from paste.translogger import TransLogger

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.scan('.views')
    app = config.make_wsgi_app()
#    app = TransLogger(app, setup_console_handler=False)
    return app
