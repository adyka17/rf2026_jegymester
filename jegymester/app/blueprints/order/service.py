from app.extensions import db
from app.models.order import Order
from app.blueprints.order.schemas import (
    OrderListSchema,
    OrderResponseSchema,
    OrderDetailSchema,
)
from sqlalchemy import select


class OrderService:
    @staticmethod
    def order_list_all():
        orders = db.session.execute(select(Order)).scalars().all()
        return True, OrderListSchema(many=True).dump(orders)

    @staticmethod
    def order_get_item(item_id: int):
        order = db.session.get(Order, item_id)
        if not order:
            return False, "A megrendelés nem található!"

        payload = {
            "id": order.id,
            "payment_status": order.payment_status,
            "tickets": [
                {
                    "ticket_id": item.ticket_id,
                    "ticket_status": item.ticket_status,
                }
                for item in order.tickets
            ],
        }
        return True, OrderDetailSchema().dump(payload)

    @staticmethod
    def order_add(data: dict):
        try:
            order = Order(**data)
            db.session.add(order)
            db.session.commit()
            return True, OrderResponseSchema().dump(order)
        except Exception:
            db.session.rollback()
            return False, "order_add() hiba!"

    @staticmethod
    def order_update(item_id: int, data: dict):
        order = db.session.get(Order, item_id)
        if not order:
            return False, "A megrendelés nem található!"

        try:
            if "payment_status" in data:
                order.payment_status = data["payment_status"]

            db.session.commit()
            return True, OrderResponseSchema().dump(order)
        except Exception:
            db.session.rollback()
            return False, "order_update() hiba!"

    @staticmethod
    def order_delete(item_id: int):
        order = db.session.get(Order, item_id)
        if not order:
            return False, "A megrendelés nem található!"

        try:
            db.session.delete(order)
            db.session.commit()
            return True, {"message": "A megrendelés törölve."}
        except Exception:
            db.session.rollback()
            return False, "order_delete() hiba!"