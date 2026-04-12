from flask import jsonify, request
from app.blueprints.order import bp
from app.blueprints.order.schemas import OrderRequestSchema, OrderUpdateSchema
from app.blueprints.order.service import OrderService


@bp.route("/")
def index():
    return jsonify(message="Order Blueprint")


@bp.get("/list_all")
def order_list_all():
    success, response = OrderService.order_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def order_get_item(item_id):
    success, response = OrderService.order_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def order_add_new():
    data = OrderRequestSchema().load(request.get_json() or {})
    success, response = OrderService.order_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def order_update(item_id):
    data = OrderUpdateSchema().load(request.get_json() or {})
    success, response = OrderService.order_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def order_delete(item_id):
    success, response = OrderService.order_delete(item_id)
    return jsonify(response), 200 if success else 400