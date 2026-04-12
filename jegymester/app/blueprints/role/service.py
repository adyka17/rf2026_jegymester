from app.extensions import db
from app.models.role import Role
from app.blueprints.role.schemas import RoleListSchema, RoleResponseSchema
from sqlalchemy import select


class RoleService:
    @staticmethod
    def role_list_all():
        roles = db.session.execute(select(Role)).scalars().all()
        return True, RoleListSchema(many=True).dump(roles)

    @staticmethod
    def role_get_item(item_id: int):
        role = db.session.get(Role, item_id)
        if not role:
            return False, "A szerepkör nem található!"
        return True, RoleResponseSchema().dump(role)

    @staticmethod
    def role_add(data: dict):
        try:
            role = Role(**data)
            db.session.add(role)
            db.session.commit()
            return True, RoleResponseSchema().dump(role)
        except Exception:
            db.session.rollback()
            return False, "role_add() hiba!"

    @staticmethod
    def role_update(item_id: int, data: dict):
        role = db.session.get(Role, item_id)
        if not role:
            return False, "A szerepkör nem található!"

        try:
            if "rolename" in data:
                role.rolename = data["rolename"]
            db.session.commit()
            return True, RoleResponseSchema().dump(role)
        except Exception:
            db.session.rollback()
            return False, "role_update() hiba!"

    @staticmethod
    def role_delete(item_id: int):
        role = db.session.get(Role, item_id)
        if not role:
            return False, "A szerepkör nem található!"

        try:
            db.session.delete(role)
            db.session.commit()
            return True, {"message": "A szerepkör törölve."}
        except Exception:
            db.session.rollback()
            return False, "role_delete() hiba!"