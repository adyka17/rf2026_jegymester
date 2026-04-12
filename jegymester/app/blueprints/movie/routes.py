from flask import jsonify, request
from app.blueprints.movie import bp
from app.blueprints.movie.schemas import (
    MovieRequestSchema,
    MovieUpdateSchema,
)
from app.blueprints.movie.service import MovieService


@bp.route("/")
def index():
    return jsonify(message="Movie Blueprint")


@bp.get("/list_all")
def movie_list_all():
    success, response = MovieService.movie_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def movie_get_item(item_id):
    success, response = MovieService.movie_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def movie_add_new():
    data = MovieRequestSchema().load(request.get_json() or {})
    success, response = MovieService.movie_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def movie_update(item_id):
    data = MovieUpdateSchema().load(request.get_json() or {})
    success, response = MovieService.movie_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def movie_delete(item_id):
    success, response = MovieService.movie_delete(item_id)
    return jsonify(response), 200 if success else 400


@bp.get("/screenings/<int:item_id>")
def movie_screenings(item_id):
    success, response = MovieService.movie_screenings(item_id)
    return jsonify(response), 200 if success else 404