from app.extensions import db
from app.models.userrole import UserRole
from app.blueprints.userrole.schemas import (
    UserRoleListSchema,
    UserRoleResponseSchema,
)
from sqlalchemy import select


class UserRoleService:
    @staticmethod
    def userrole_list_all():
        userroles = db.session.execute(select(UserRole)).scalars().all()
        return True, UserRoleListSchema(many=True).dump(userroles)

    @staticmethod
    def userrole_get_item(user_id: int, role_id: int):
        userrole = db.session.get(UserRole, {"user_id": user_id, "role_id": role_id})
        if not userrole:
            return False, "A userrole nem található!"
        return True, UserRoleResponseSchema().dump(userrole)

    @staticmethod
    def userrole_add(data: dict):
        try:
            existing = db.session.get(
                UserRole,
                {"user_id": data["user_id"], "role_id": data["role_id"]},
            )
            if existing:
                return False, "Ez a user-role kapcsolat már létezik!"

            userrole = UserRole(**data)
            db.session.add(userrole)
            db.session.commit()
            return True, UserRoleResponseSchema().dump(userrole)
        except Exception:
            db.session.rollback()
            return False, "userrole_add() hiba!"

    @staticmethod
    def userrole_update(user_id: int, role_id: int, data: dict):
        userrole = db.session.get(UserRole, {"user_id": user_id, "role_id": role_id})
        if not userrole:
            return False, "A userrole nem található!"

        try:
            new_role_id = data["new_role_id"]

            existing = db.session.get(
                UserRole,
                {"user_id": user_id, "role_id": new_role_id},
            )
            if existing:
                return False, "A cél user-role kapcsolat már létezik!"

            db.session.delete(userrole)
            db.session.flush()

            new_userrole = UserRole(user_id=user_id, role_id=new_role_id)
            db.session.add(new_userrole)
            db.session.commit()

            return True, UserRoleResponseSchema().dump(new_userrole)
        except Exception:
            db.session.rollback()
            return False, "userrole_update() hiba!"

    @staticmethod
    def userrole_delete(user_id: int, role_id: int):
        userrole = db.session.get(UserRole, {"user_id": user_id, "role_id": role_id})
        if not userrole:
            return False, "A userrole nem található!"

        try:
            db.session.delete(userrole)
            db.session.commit()
            return True, {"message": "A userrole törölve."}
        except Exception:
            db.session.rollback()
            return False, "userrole_delete() hiba!"
