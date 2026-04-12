from app.extensions import db
from app.models.ticketcategory import TicketCategory
from app.blueprints.ticketcategory.schemas import (
    TicketCategoryListSchema,
    TicketCategoryResponseSchema,
)
from sqlalchemy import select


class TicketCategoryService:
    @staticmethod
    def ticketcategory_list_all():
        categories = db.session.execute(select(TicketCategory)).scalars().all()
        return True, TicketCategoryListSchema(many=True).dump(categories)

    @staticmethod
    def ticketcategory_get_item(item_id: int):
        category = db.session.get(TicketCategory, item_id)
        if not category:
            return False, "A jegykategória nem található!"
        return True, TicketCategoryResponseSchema().dump(category)

    @staticmethod
    def ticketcategory_add(data: dict):
        try:
            category = TicketCategory(**data)
            db.session.add(category)
            db.session.commit()
            return True, TicketCategoryResponseSchema().dump(category)
        except Exception:
            db.session.rollback()
            return False, "ticketcategory_add() hiba!"

    @staticmethod
    def ticketcategory_update(item_id: int, data: dict):
        category = db.session.get(TicketCategory, item_id)
        if not category:
            return False, "A jegykategória nem található!"

        try:
            for field in ["catname", "price"]:
                if field in data:
                    setattr(category, field, data[field])

            db.session.commit()
            return True, TicketCategoryResponseSchema().dump(category)
        except Exception:
            db.session.rollback()
            return False, "ticketcategory_update() hiba!"

    @staticmethod
    def ticketcategory_delete(item_id: int):
        category = db.session.get(TicketCategory, item_id)
        if not category:
            return False, "A jegykategória nem található!"

        try:
            db.session.delete(category)
            db.session.commit()
            return True, {"message": "A jegykategória törölve."}
        except Exception:
            db.session.rollback()
            return False, "ticketcategory_delete() hiba!"