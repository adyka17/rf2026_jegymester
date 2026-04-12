from app.extensions import db
from app.models.ticketorder import TicketOrder
from app.blueprints.ticketorder.schemas import (
    TicketOrderListSchema,
    TicketOrderResponseSchema,
)
from sqlalchemy import select


class TicketOrderService:
    @staticmethod
    def ticketorder_list_all():
        ticketorders = db.session.execute(select(TicketOrder)).scalars().all()
        return True, TicketOrderListSchema(many=True).dump(ticketorders)

    @staticmethod
    def ticketorder_get_item(order_id: int, ticket_id: int):
        ticketorder = db.session.get(TicketOrder, {"order_id": order_id, "ticket_id": ticket_id})
        if not ticketorder:
            return False, "A ticketorder nem található!"
        return True, TicketOrderResponseSchema().dump(ticketorder)

    @staticmethod
    def ticketorder_add(data: dict):
        try:
            ticketorder = TicketOrder(**data)
            db.session.add(ticketorder)
            db.session.commit()
            return True, TicketOrderResponseSchema().dump(ticketorder)
        except Exception:
            db.session.rollback()
            return False, "ticketorder_add() hiba!"

    @staticmethod
    def ticketorder_update(order_id: int, ticket_id: int, data: dict):
        ticketorder = db.session.get(TicketOrder, {"order_id": order_id, "ticket_id": ticket_id})
        if not ticketorder:
            return False, "A ticketorder nem található!"

        try:
            if "ticket_status" in data:
                ticketorder.ticket_status = data["ticket_status"]
            db.session.commit()
            return True, TicketOrderResponseSchema().dump(ticketorder)
        except Exception:
            db.session.rollback()
            return False, "ticketorder_update() hiba!"

    @staticmethod
    def ticketorder_delete(order_id: int, ticket_id: int):
        ticketorder = db.session.get(TicketOrder, {"order_id": order_id, "ticket_id": ticket_id})
        if not ticketorder:
            return False, "A ticketorder nem található!"

        try:
            db.session.delete(ticketorder)
            db.session.commit()
            return True, {"message": "A ticketorder törölve."}
        except Exception:
            db.session.rollback()
            return False, "ticketorder_delete() hiba!"

