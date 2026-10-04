import re
with open('backend/app.py', 'r') as f:
    content = f.read()

old_404 = """@app.errorhandler(404)
def not_found(e):
    from flask import request
    # Return JSON so the frontend doesn't crash on parsing HTML
    return jsonify({
        "error": f"Route not found: {request.path}",
        "method": request.method,
        "url": request.url
    }), 404"""

new_404 = """@app.errorhandler(404)
def not_found(e):
    from flask import request
    # Extract headers that might contain the original path
    env = request.environ
    debug_info = {
        k: v for k, v in env.items() if isinstance(v, str) and ('api' in v or 'auth' in v or k.startswith('HTTP_X_'))
    }
    return jsonify({
        "error": f"Route not found: {request.path}",
        "method": request.method,
        "url": request.url,
        "debug_env": debug_info
    }), 404"""

if old_404 in content:
    content = content.replace(old_404, new_404)
    with open('backend/app.py', 'w') as f:
        f.write(content)
    print("Patched 404")
else:
    print("Could not find old 404")
