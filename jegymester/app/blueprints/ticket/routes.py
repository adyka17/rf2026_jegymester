from flask import jsonify, request
from app.blueprints.ticket import bp
from app.blueprints.ticket.schemas import TicketRequestSchema, TicketUpdateSchema
from app.blueprints.ticket.service import TicketService


@bp.route("/")
def index():
    return jsonify(message="Ticket Blueprint")


@bp.get("/list")
def ticket_list_all():
    success, response = TicketService.ticket_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/reserved")
def ticket_reserved_list_all():
    success, response = TicketService.ticket_reserved_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def ticket_get_item(item_id):
    success, response = TicketService.get_ticket(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def ticket_add_new():
    data = TicketRequestSchema().load(request.get_json() or {})
    success, response = TicketService.ticket_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def ticket_update(item_id):
    data = TicketUpdateSchema().load(request.get_json() or {})
    success, response = TicketService.ticket_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def ticket_delete(item_id):
    success, response = TicketService.ticket_delete(item_id)
    return jsonify(response), 200 if success else 400
