import sys
import os

# Ensure backend module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

# Vercel WSGI Middleware to fix PATH_INFO after a rewrite
class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        # When Vercel rewrites to /api/index.py, it changes PATH_INFO
        # We need to recover the original path
        req_uri = environ.get('REQUEST_URI') or environ.get('RAW_URI') or environ.get('HTTP_X_ORIGINAL_URI') or environ.get('HTTP_X_REWRITE_URL') or environ.get('HTTP_X_FORWARDED_URI')
        if req_uri:
            # req_uri might be "/api/auth/send-code?foo=bar"
            environ['PATH_INFO'] = req_uri.split('?')[0]
            
        return self.app(environ, start_response)

app.wsgi_app = VercelWSGIMiddleware(app.wsgi_app)
