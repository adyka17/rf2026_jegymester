from app.extensions import db
from app.models.seat import Seat
from app.blueprints.seat.schemas import SeatListSchema, SeatResponseSchema
from sqlalchemy import select


class SeatService:
    @staticmethod
    def seat_list_all():
        seats = db.session.execute(select(Seat)).scalars().all()
        return True, SeatListSchema(many=True).dump(seats)

    @staticmethod
    def seat_get_item(item_id: int):
        seat = db.session.get(Seat, item_id)
        if not seat:
            return False, "A szék nem található!"
        return True, SeatResponseSchema().dump(seat)

    @staticmethod
    def seat_add(data: dict):
        try:
            seat = Seat(**data)
            db.session.add(seat)
            db.session.commit()
            return True, SeatResponseSchema().dump(seat)
        except Exception:
            db.session.rollback()
            return False, "seat_add() hiba!"

    @staticmethod
    def seat_update(item_id: int, data: dict):
        seat = db.session.get(Seat, item_id)
        if not seat:
            return False, "A szék nem található!"

        try:
            for field in ["theater_id", "seat_number", "reserved"]:
                if field in data:
                    setattr(seat, field, data[field])

            db.session.commit()
            return True, SeatResponseSchema().dump(seat)
        except Exception:
            db.session.rollback()
            return False, "seat_update() hiba!"

    @staticmethod
    def seat_delete(item_id: int):
        seat = db.session.get(Seat, item_id)
        if not seat:
            return False, "A szék nem található!"

        try:
            db.session.delete(seat)
            db.session.commit()
            return True, {"message": "A szék törölve."}
        except Exception:
            db.session.rollback()
            return False, "seat_delete() hiba!"