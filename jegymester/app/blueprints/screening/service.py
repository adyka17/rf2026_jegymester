from app.extensions import db
from app.models.screening import Screening
from app.blueprints.screening.schemas import (
    ScreeningListSchema,
    ScreeningResponseSchema,
    ScreeningDetailSchema,
)
from sqlalchemy import select


class ScreeningService:
    @staticmethod
    def screening_list_all():
        screenings = db.session.execute(select(Screening)).scalars().all()
        return True, ScreeningListSchema(many=True).dump(screenings)

    @staticmethod
    def screening_get_item(item_id: int):
        screening = db.session.get(Screening, item_id)
        if not screening:
            return False, "A vetítés nem található!"

        payload = {
            "id": screening.id,
            "start_time": screening.start_time,
            "movie": {
                "id": screening.movie.id,
                "title": screening.movie.title,
            } if screening.movie else None,
            "theater": {
                "id": screening.theater.id,
                "theatname": screening.theater.theatname,
            } if screening.theater else None,
        }
        return True, ScreeningDetailSchema().dump(payload)

    @staticmethod
    def screening_add(data: dict):
        try:
            screening = Screening(**data)
            db.session.add(screening)
            db.session.commit()
            return True, ScreeningResponseSchema().dump(screening)
        except Exception:
            db.session.rollback()
            return False, "screening_add() hiba!"

    @staticmethod
    def screening_update(item_id: int, data: dict):
        screening = db.session.get(Screening, item_id)
        if not screening:
            return False, "A vetítés nem található!"

        try:
            for field in ["movie_id", "theater_id", "start_time"]:
                if field in data:
                    setattr(screening, field, data[field])

            db.session.commit()
            return True, ScreeningResponseSchema().dump(screening)
        except Exception:
            db.session.rollback()
            return False, "screening_update() hiba!"

    @staticmethod
    def screening_delete(item_id: int):
        screening = db.session.get(Screening, item_id)
        if not screening:
            return False, "A vetítés nem található!"

        try:
            db.session.delete(screening)
            db.session.commit()
            return True, {"message": "A vetítés törölve."}
        except Exception:
            db.session.rollback()
            return False, "screening_delete() hiba!"