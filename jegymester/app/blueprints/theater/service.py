from app.extensions import db
from app.models.theater import Theater
from app.blueprints.theater.schemas import (
    TheaterListSchema,
    TheaterResponseSchema,
    TheaterToSeatSchema,
)
from sqlalchemy import select


class TheaterService:
    @staticmethod
    def theater_list_all():
        theaters = db.session.execute(select(Theater)).scalars().all()
        return True, TheaterListSchema(many=True).dump(theaters)

    @staticmethod
    def theater_get_item(item_id: int):
        theater = db.session.get(Theater, item_id)
        if not theater:
            return False, "A terem nem található!"
        return True, TheaterResponseSchema().dump(theater)

    @staticmethod
    def theater_add(data: dict):
        try:
            theater = Theater(**data)
            db.session.add(theater)
            db.session.commit()
            return True, TheaterResponseSchema().dump(theater)
        except Exception:
            db.session.rollback()
            return False, "theater_add() hiba!"

    @staticmethod
    def theater_update(item_id: int, data: dict):
        theater = db.session.get(Theater, item_id)
        if not theater:
            return False, "A terem nem található!"

        try:
            if "theatname" in data:
                theater.theatname = data["theatname"]
            db.session.commit()
            return True, TheaterResponseSchema().dump(theater)
        except Exception:
            db.session.rollback()
            return False, "theater_update() hiba!"

    @staticmethod
    def theater_delete(item_id: int):
        theater = db.session.get(Theater, item_id)
        if not theater:
            return False, "A terem nem található!"

        try:
            db.session.delete(theater)
            db.session.commit()
            return True, {"message": "A terem törölve."}
        except Exception:
            db.session.rollback()
            return False, "theater_delete() hiba!"

    @staticmethod
    def theater_seats(item_id: int):
        theater = db.session.get(Theater, item_id)
        if not theater:
            return False, "A terem nem található!"

        payload = {
            "id": theater.id,
            "theatname": theater.theatname,
            "seats": [
                {
                    "id": seat.id,
                    "seat_number": seat.seat_number,
                    "reserved": seat.reserved,
                }
                for seat in theater.seats
            ],
        }
        return True, TheaterToSeatSchema().dump(payload)
