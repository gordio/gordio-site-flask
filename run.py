#!venv/bin/python
import sys
sys.path.append("/var/home/gordio/gordio.pp.ua/app")
sys.path.append("/var/home/gordio/venv")
sys.path.append("/var/home/gordio/venv/lib")
sys.path.append("/var/home/gordio/venv/lib/python2.6")
sys.path.append("/var/home/gordio/venv/lib/python2.6/site-packages")

from wsgiref.handlers import CGIHandler
from main import app
from models import db # make sure to import




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
else:
    class WebFactionMiddleware(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, environ, start_response):
            environ['SCRIPT_NAME'] = ''
            return self.app(environ, start_response)

    app.wsgi_app = WebFactionMiddleware(app.wsgi_app)
    CGIHandler().run(app)