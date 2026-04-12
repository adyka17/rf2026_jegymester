from flask import jsonify, request
from app.blueprints.user import bp
from app.blueprints.user.schemas import (
    UserRequestSchema,
    UserLoginSchema,
    UserUpdateSchema,
)
from app.blueprints.user.service import UserService


@bp.route("/")
def index():
    return jsonify(message="User Blueprint")


@bp.post("/registrate")
def user_registrate():
    data = UserRequestSchema().load(request.get_json() or {})
    success, response = UserService.user_registrate(data)
    return jsonify(response), 201 if success else 400


@bp.post("/login")
def user_login():
    data = UserLoginSchema().load(request.get_json() or {})
    success, response = UserService.user_login(data)
    return jsonify(response), 200 if success else 400


@bp.get("/list_all")
def user_list_all():
    success, response = UserService.user_list_all()
    return jsonify(response), 200 if success else 400


@bp.get("/get/<int:item_id>")
def user_get_item(item_id):
    success, response = UserService.user_get_item(item_id)
    return jsonify(response), 200 if success else 404


@bp.put("/update/<int:item_id>")
def user_update(item_id):
    data = UserUpdateSchema().load(request.get_json() or {})
    success, response = UserService.user_update(item_id, data)
    return jsonify(response), 200 if success else 400


@bp.delete("/delete/<int:item_id>")
def user_delete(item_id):
    success, response = UserService.user_delete(item_id)
    return jsonify(response), 200 if success else 400