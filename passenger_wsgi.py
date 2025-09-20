# import os
# import sys


# sys.path.insert(0, os.path.dirname(__file__))


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python %s\n' % sys.version.split()[0]
#     response = '\n'.join([message, version])
#     return [response.encode()]


import os
import sys

# --- Full path to your project directory ---
project_home = os.path.dirname(os.path.abspath(__file__))

# Add project directory to sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# If apps/ folder is used, also add it
apps_path = os.path.join(project_home, "apps")
if apps_path not in sys.path:
    sys.path.insert(0, apps_path)

# Set environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "likhoncombd.settings")

# Load Django’s WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
