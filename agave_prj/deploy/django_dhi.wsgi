import os
import sys

sys.stdout = sys.stderr

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
print sys.path
from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "agave_prj.settings"

#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if environ.get("HTTP_X_FORWARDED_PROTOCOL") == "https" or environ.get("HTTP_X_FORWARDED_SSL") == "on":
        environ["wsgi.url_scheme"] = "https"
    return _application(environ, start_response)

