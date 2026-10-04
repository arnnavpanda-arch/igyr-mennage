import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # Fix PATH_INFO based on original request
        req_uri = environ.get('REQUEST_URI') or environ.get('RAW_URI') or environ.get('HTTP_X_ORIGINAL_URI') or environ.get('HTTP_X_REWRITE_URL') or environ.get('HTTP_X_FORWARDED_URI')
        if req_uri:
            environ['PATH_INFO'] = req_uri.split('?')[0]
        return self.app(environ, start_response)

app.wsgi_app = VercelWSGIMiddleware(app.wsgi_app)
