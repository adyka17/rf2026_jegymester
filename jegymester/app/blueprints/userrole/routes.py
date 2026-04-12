from flask import jsonify, request
from app.blueprints.userrole import bp
from app.blueprints.userrole.schemas import (
    UserRoleRequestSchema,
    UserRoleUpdateSchema,
)
from app.blueprints.userrole.service import UserRoleService


@bp.route("/")
def index():
    return jsonify(message="UserRole Blueprint")


@bp.get("/list_all")
def userrole_list_all():
    success, response = UserRoleService.userrole_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:user_id>/<int:role_id>")
def userrole_get_item(user_id, role_id):
    success, response = UserRoleService.userrole_get_item(user_id, role_id)
    return jsonify(response), 200 if success else 404


@bp.post("/add")
def userrole_add_new():
    data = UserRoleRequestSchema().load(request.get_json() or {})
    success, response = UserRoleService.userrole_add(data)
    return jsonify(response), 201 if success else 400


@bp.put("/update/<int:user_id>/<int:role_id>")
def userrole_update(user_id, role_id):
    data = UserRoleUpdateSchema().load(request.get_json() or {})
    success, response = UserRoleService.userrole_update(user_id, role_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:user_id>/<int:role_id>")
def userrole_delete(user_id, role_id):
    success, response = UserRoleService.userrole_delete(user_id, role_id)
    return jsonify(response), 200 if success else 400