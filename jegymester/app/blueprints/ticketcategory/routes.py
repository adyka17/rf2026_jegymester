from flask import jsonify, request
from app.blueprints.ticketcategory import bp
from app.blueprints.ticketcategory.schemas import (
    TicketCategoryRequestSchema,
    TicketCategoryUpdateSchema,
)
from app.blueprints.ticketcategory.service import TicketCategoryService


@bp.route("/")
def index():
    return jsonify(message="TicketCategory Blueprint")


@bp.get("/list_all")
def ticketcategory_list_all():
    success, response = TicketCategoryService.ticketcategory_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def ticketcategory_get_item(item_id):
    success, response = TicketCategoryService.ticketcategory_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def ticketcategory_add_new():
    data = TicketCategoryRequestSchema().load(request.get_json() or {})
    success, response = TicketCategoryService.ticketcategory_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def ticketcategory_update(item_id):
    data = TicketCategoryUpdateSchema().load(request.get_json() or {})
    success, response = TicketCategoryService.ticketcategory_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def ticketcategory_delete(item_id):
    success, response = TicketCategoryService.ticketcategory_delete(item_id)
    return jsonify(response), 200 if success else 400
