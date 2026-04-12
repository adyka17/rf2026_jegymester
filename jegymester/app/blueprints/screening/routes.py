from flask import jsonify, request
from app.blueprints.screening import bp
from app.blueprints.screening.schemas import ScreeningRequestSchema, ScreeningUpdateSchema
from app.blueprints.screening.service import ScreeningService


@bp.route("/")
def index():
    return jsonify(message="Screening Blueprint")


@bp.get("/list_all")
def screening_list_all():
    success, response = ScreeningService.screening_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def screening_get_item(item_id):
    success, response = ScreeningService.screening_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def screening_add_new():
    data = ScreeningRequestSchema().load(request.get_json() or {})
    success, response = ScreeningService.screening_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def screening_update(item_id):
    data = ScreeningUpdateSchema().load(request.get_json() or {})
    success, response = ScreeningService.screening_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def screening_delete(item_id):
    success, response = ScreeningService.screening_delete(item_id)
    return jsonify(response), 200 if success else 400