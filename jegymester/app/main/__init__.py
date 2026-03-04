from flask import Blueprint

bp = Blueprint("main", __name__)
bp.tag = "default"

from app.main import routes