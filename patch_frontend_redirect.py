import re
with open('backend/app.py', 'r') as f:
    content = f.read()

redirect_code = """
@app.route('/frontend/', defaults={'path': ''})
@app.route('/frontend/<path:path>')
def frontend_redirect(path):
    from flask import redirect
    return redirect(f"/{path}", code=301)
"""

if "@app.route('/frontend/')" not in content:
    content = content.replace("app = Flask(__name__)\nCORS(app)  # Enable CORS for frontend requests", "app = Flask(__name__)\nCORS(app)  # Enable CORS for frontend requests\n" + redirect_code)
    with open('backend/app.py', 'w') as f:
        f.write(content)
    print("Added redirect")
