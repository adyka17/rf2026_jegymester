from app.main import bp
from flask import jsonify


@bp.route('/')
def index():
    return "Flask projekt - JegyMester"


@bp.route('/health')
def health():
    return jsonify(status="ok")