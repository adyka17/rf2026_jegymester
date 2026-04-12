from flask import jsonify, request
from app.blueprints.seat import bp
from app.blueprints.seat.schemas import SeatRequestSchema, SeatUpdateSchema
from app.blueprints.seat.service import SeatService


@bp.route("/")
def index():
    return jsonify(message="Seat Blueprint")


@bp.get("/list")
def seat_list_all():
    success, response = SeatService.seat_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def seat_get_item(item_id):
    success, response = SeatService.seat_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def seat_add_new():
    data = SeatRequestSchema().load(request.get_json() or {})
    success, response = SeatService.seat_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def seat_update(item_id):
    data = SeatUpdateSchema().load(request.get_json() or {})
    success, response = SeatService.seat_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def seat_delete(item_id):
    success, response = SeatService.seat_delete(item_id)
    return jsonify(response), 200 if success else 400