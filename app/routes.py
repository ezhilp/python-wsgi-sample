from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return jsonify({
        "message": "Hello from WSGI app",
        "status": "ok"
    })


@bp.get("/health")
def health():
    return jsonify({"healthy": True}), 200