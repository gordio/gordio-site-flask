#!/var/home/gordio/venv/bin/python
import sys
sys.path.append("/var/home/gordio/gordio.pp.ua/app")
sys.path.append("/var/home/gordio/venv")
sys.path.append("/var/home/gordio/venv/lib")
sys.path.append("/var/home/gordio/venv/lib/python2.6")
sys.path.append("/var/home/gordio/venv/lib/python2.6/site-packages")

from wsgiref.handlers import CGIHandler
from main import app

class WebFactionMiddleware(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = ''
		return self.app(environ, start_response)

app.wsgi_app = WebFactionMiddleware(app.wsgi_app)


CGIHandler().run(app)
