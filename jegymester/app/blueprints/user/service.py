from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.blueprints.user.schemas import (
    UserResponseSchema,
    UserListSchema,
    UserDetailSchema,
)
from sqlalchemy import select


class UserService:
    @staticmethod
    def user_registrate(data: dict):
        try:
            existing = db.session.execute(
                select(User).filter_by(email=data["email"])
            ).scalar_one_or_none()

            if existing:
                return False, "Ez az e-mail cím már létezik!"

            user = User(email=data["email"], phone=data["phone"])
            user.set_password(data["password"])

            default_role = db.session.execute(
                select(Role).filter_by(rolename="User")
            ).scalar_one_or_none()

            if default_role:
                user.roles.append(default_role)

            db.session.add(user)
            db.session.commit()
            return True, UserResponseSchema().dump(user)
        except Exception:
            db.session.rollback()
            return False, "user_registrate() hiba!"

    @staticmethod
    def user_login(data: dict):
        try:
            user = db.session.execute(
                select(User).filter_by(email=data["email"])
            ).scalar_one_or_none()

            if not user or not user.check_password(data["password"]):
                return False, "Hibás e-mail vagy jelszó!"

            return True, UserResponseSchema().dump(user)
        except Exception:
            return False, "user_login() hiba!"

    @staticmethod
    def user_list_all():
        users = db.session.execute(select(User)).scalars().all()
        return True, UserListSchema(many=True).dump(users)

    @staticmethod
    def user_get_item(item_id: int):
        user = db.session.get(User, item_id)
        if not user:
            return False, "A felhasználó nem található!"

        payload = {
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "roles": [{"id": role.id, "rolename": role.rolename} for role in user.roles],
            "tickets": [
                {
                    "id": ticket.id,
                    "screening_id": ticket.screening_id,
                    "ticketcategory_id": ticket.ticketcategory_id,
                    "seat_id": ticket.seat_id,
                }
                for ticket in user.tickets
            ],
        }
        return True, UserDetailSchema().dump(payload)

    @staticmethod
    def user_update(item_id: int, data: dict):
        user = db.session.get(User, item_id)
        if not user:
            return False, "A felhasználó nem található!"

        try:
            if "email" in data:
                user.email = data["email"]
            if "phone" in data:
                user.phone = data["phone"]
            if "password" in data:
                user.set_password(data["password"])

            db.session.commit()
            return True, UserResponseSchema().dump(user)
        except Exception:
            db.session.rollback()
            return False, "user_update() hiba!"

    @staticmethod
    def user_delete(item_id: int):
        user = db.session.get(User, item_id)
        if not user:
            return False, "A felhasználó nem található!"

        try:
            db.session.delete(user)
            db.session.commit()
            return True, {"message": "A felhasználó törölve."}
        except Exception:
            db.session.rollback()
            return False, "user_delete() hiba!"