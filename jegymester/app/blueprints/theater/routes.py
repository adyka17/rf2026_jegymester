from flask import jsonify, request
from app.blueprints.theater import bp
from app.blueprints.theater.schemas import TheaterRequestSchema, TheaterUpdateSchema
from app.blueprints.theater.service import TheaterService


@bp.route("/")
def index():
    return jsonify(message="Theater Blueprint")


@bp.get("/list")
def theater_list_all():
    success, response = TheaterService.theater_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def theater_get_item(item_id):
    success, response = TheaterService.theater_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def theater_add_new():
    data = TheaterRequestSchema().load(request.get_json() or {})
    success, response = TheaterService.theater_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def theater_update(item_id):
    data = TheaterUpdateSchema().load(request.get_json() or {})
    success, response = TheaterService.theater_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def theater_delete(item_id):
    success, response = TheaterService.theater_delete(item_id)
    return jsonify(response), 200 if success else 400


@bp.get("/seats/<int:item_id>")
def theater_seats(item_id):
    success, response = TheaterService.theater_seats(item_id)
    return jsonify(response), 200 if success else 404