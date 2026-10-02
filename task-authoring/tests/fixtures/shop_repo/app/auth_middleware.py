from flask import request, abort


def require_token(app):
    @app.before_request
    def check():
        if request.path.startswith("/public"):
            return
        token = request.headers.get("Authorization", "")
        if not token.startswith("Bearer ") or len(token) < 20:
            abort(401)
