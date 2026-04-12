from app.extensions import db
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.blueprints.ticket.schemas import (
    TicketListSchema,
    TicketResponseSchema,
    TicketDetailSchema,
)
from sqlalchemy import select

class TicketService:
    @staticmethod
    def ticket_list_all():
        tickets = db.session.execute(select(Ticket)).scalars().all()
        return True, TicketListSchema(many=True).dump(tickets)

    @staticmethod
    def ticket_reserved_list_all():
        tickets = db.session.execute(
            select(Ticket).join(Seat).filter(Seat.reserved.is_(True))
        ).scalars().all()
        return True, TicketListSchema(many=True).dump(tickets)

    @staticmethod
    def ticket_get_item(item_id: int):
        ticket = db.session.get(Ticket, item_id)
        if not ticket:
            return False, "A jegy nem található!"
        return True, TicketResponseSchema().dump(ticket)

    @staticmethod
    def ticket_add(data: dict):
        try:
            seat = db.session.get(Seat, data["seat_id"])
            if not seat:
                return False, "A kiválasztott szék nem található!"
            if seat.reserved:
                return False, "A kiválasztott szék már foglalt!"

            ticket = Ticket(**data)
            db.session.add(ticket)
            seat.reserved = True
            db.session.commit()
            return True, TicketResponseSchema().dump(ticket)
        except Exception:
            db.session.rollback()
            return False, "ticket_add() hiba!"

    @staticmethod
    def ticket_update(item_id: int, data: dict):
        ticket = db.session.get(Ticket, item_id)
        if not ticket:
            return False, "A jegy nem található!"

        try:
            old_seat = db.session.get(Seat, ticket.seat_id)

            if "seat_id" in data and data["seat_id"] != ticket.seat_id:
                new_seat = db.session.get(Seat, data["seat_id"])
                if not new_seat:
                    return False, "Az új szék nem található!"
                if new_seat.reserved:
                    return False, "Az új szék már foglalt!"

                if old_seat:
                    old_seat.reserved = False
                new_seat.reserved = True
                ticket.seat_id = data["seat_id"]

            for field in ["screening_id", "user_id", "ticketcategory_id"]:
                if field in data:
                    setattr(ticket, field, data[field])

            db.session.commit()
            return True, TicketResponseSchema().dump(ticket)
        except Exception:
            db.session.rollback()
            return False, "ticket_update() hiba!"

    @staticmethod
    def ticket_delete(item_id: int):
        ticket = db.session.get(Ticket, item_id)
        if not ticket:
            return False, "A jegy nem található!"

        try:
            seat = db.session.get(Seat, ticket.seat_id)
            if seat:
                seat.reserved = False
            db.session.delete(ticket)
            db.session.commit()
            return True, {"message": "A jegy törölve."}
        except Exception:
            db.session.rollback()
            return False, "ticket_delete() hiba!"

    @staticmethod
    def get_ticket(item_id: int):
        ticket = db.session.get(Ticket, item_id)
        if not ticket:
            return False, "A jegy nem található!"

        payload = {
            "id": ticket.id,
            "screening": {
                "id": ticket.screening.id,
                "start_time": ticket.screening.start_time.isoformat(),
                "movie_id": ticket.screening.movie_id,
                "theater_id": ticket.screening.theater_id,
            } if ticket.screening else None,
            "user": {
                "id": ticket.user.id,
                "email": ticket.user.email,
                "phone": ticket.user.phone,
            } if ticket.user else None,
            "ticketcategory": {
                "id": ticket.ticketcategory.id,
                "catname": ticket.ticketcategory.catname,
                "price": ticket.ticketcategory.price,
            } if ticket.ticketcategory else None,
            "seat": {
                "id": ticket.seat.id,
                "seat_number": ticket.seat.seat_number,
                "reserved": ticket.seat.reserved,
            } if ticket.seat else None,
        }
        return True, TicketDetailSchema().dump(payload)
