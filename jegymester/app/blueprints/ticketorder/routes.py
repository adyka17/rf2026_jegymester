from flask import jsonify, request
from app.blueprints.ticketorder import bp
from app.blueprints.ticketorder.schemas import (
    TicketOrderRequestSchema,
    TicketOrderUpdateSchema,
)
from app.blueprints.ticketorder.service import TicketOrderService


@bp.route("/")
def index():
    return jsonify(message="TicketOrder Blueprint")


@bp.get("/list")
def ticketorder_list_all():
    success, response = TicketOrderService.ticketorder_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:order_id>/<int:ticket_id>")
def ticketorder_get_item(order_id, ticket_id):
    success, response = TicketOrderService.ticketorder_get_item(order_id, ticket_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def ticketorder_add_new():
    data = TicketOrderRequestSchema().load(request.get_json() or {})
    success, response = TicketOrderService.ticketorder_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:order_id>/<int:ticket_id>")
def ticketorder_update(order_id, ticket_id):
    data = TicketOrderUpdateSchema().load(request.get_json() or {})
    success, response = TicketOrderService.ticketorder_update(order_id, ticket_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:order_id>/<int:ticket_id>")
def ticketorder_delete(order_id, ticket_id):
    success, response = TicketOrderService.ticketorder_delete(order_id, ticket_id)
    return jsonify(response), 200 if success else 400

