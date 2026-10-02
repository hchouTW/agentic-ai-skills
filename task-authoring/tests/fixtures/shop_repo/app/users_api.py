from flask import Blueprint, jsonify
from app.db import query

bp = Blueprint("users", __name__)


@bp.get("/users")
def list_users():
    return jsonify(query("SELECT id, email, last_login FROM users"))
