from flask import jsonify, request
from app.blueprints.role import bp
from app.blueprints.role.schemas import RoleRequestSchema, RoleUpdateSchema
from app.blueprints.role.service import RoleService


@bp.route("/")
def index():
    return jsonify(message="Role Blueprint")


@bp.get("/list_all")
def role_list_all():
    success, response = RoleService.role_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def role_get_item(item_id):
    success, response = RoleService.role_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def role_add_new():
    data = RoleRequestSchema().load(request.get_json() or {})
    success, response = RoleService.role_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:item_id>")
def role_update(item_id):
    data = RoleUpdateSchema().load(request.get_json() or {})
    success, response = RoleService.role_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def role_delete(item_id):
    success, response = RoleService.role_delete(item_id)
    return jsonify(response), 200 if success else 400