from __future__ import annotations
from datetime import datetime

from app import create_app
from app.extensions import db
from config import Config

from app.models.user import User
from app.models.role import Role
from app.models.userrole import UserRole
from app.models.movie import Movie
from app.models.theater import Theater
from app.models.seat import Seat
from app.models.screening import Screening
from app.models.ticketcategory import TicketCategory
from app.models.order import Order
from app.models.ticket import Ticket
from app.models.ticketorder import TicketOrder


app = create_app(config_class=Config)
app.app_context().push()

try:

    if not Role.query.filter_by(rolename="Admin").first():
        db.session.add_all([
            Role(rolename="Admin"),
            Role(rolename="User"),
            Role(rolename="Cashier")
        ])
        db.session.commit()


    if not User.query.filter_by(email="testuser@example.com").first():
        user = User(email="testuser@example.com", phone="+36123456789")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    user = User.query.filter_by(email="testuser@example.com").first()
    admin_role = Role.query.filter_by(rolename="Admin").first()
    user_role = Role.query.filter_by(rolename="User").first()
    if admin_role not in user.roles:
        user.roles.append(admin_role)
    if user_role not in user.roles:
        user.roles.append(user_role)
    db.session.commit()


    movies = [
        ("Titanic", 194, "Drama", 12, "A love story on a sinking ship"),
        ("Mátrix", 136, "Sci-Fi", 16, "Reality is a simulation"),
        ("Zalán_futása", 200, "Adventure", 18, "Run away as fast as you can from Zalan"),
        ("Egyetemistak_elete", 90, "Reality", 16, "Look behind the curtain"),
        ("A_nagy_kanape_pakolas", 60, "Documentary", 10, "How to outbring a sofa"),
    ]
    for title, duration, genre, age, desc in movies:
        if not Movie.query.filter_by(title=title).first():
            db.session.add(Movie(title=title, duration=duration, genre=genre, age_limit=age, description=desc))
    db.session.commit()


    if not Theater.query.filter_by(theatname="Főterem").first():
        theater = Theater(theatname="Főterem")
        db.session.add(theater)
    if not Theater.query.filter_by(theatname="Kisterem").first():
        theater2 = Theater(theatname="Kisterem")
        db.session.add(theater2)
    db.session.commit()


    theater1 = Theater.query.filter_by(theatname="Főterem").first()
    theater2 = Theater.query.filter_by(theatname="Kisterem").first()
    if not Seat.query.filter_by(theater_id=theater1.id, seat_number="A1").first():
        db.session.add_all([
            Seat(theater_id=theater1.id, seat_number="A1"),
            Seat(theater_id=theater1.id, seat_number="A2"),
            Seat(theater_id=theater2.id, seat_number="B1")
        ])
        db.session.commit()


    movie1 = Movie.query.filter_by(title="Titanic").first()
    movie2 = Movie.query.filter_by(title="Mátrix").first()
    if not Screening.query.filter_by(movie_id=movie1.id, theater_id=theater1.id).first():
        screening = Screening(movie_id=movie1.id, theater_id=theater1.id, start_time=datetime(2025, 3, 10, 18, 0))
        screening2 = Screening(movie_id=movie2.id, theater_id=theater2.id, start_time=datetime(2025, 3, 10, 20, 0))
        db.session.add_all([screening, screening2])
        db.session.commit()


    if not TicketCategory.query.filter_by(catname="Felnőtt").first():
        db.session.add_all([
            TicketCategory(catname="Felnőtt", price=2500),
            TicketCategory(catname="Diák", price=2000),
            TicketCategory(catname="Nyugdíjas", price=1800)
        ])
        db.session.commit()


    if not Order.query.filter_by(payment_status="Pending").first():
        order = Order(payment_status="Pending")
        db.session.add(order)
        db.session.commit()


    screening1 = Screening.query.filter_by(movie_id=movie1.id).first()
    screening2 = Screening.query.filter_by(movie_id=movie2.id).first()
    adult_category = TicketCategory.query.filter_by(catname="Felnőtt").first()
    student_category = TicketCategory.query.filter_by(catname="Diák").first()

    seat1 = Seat.query.filter_by(theater_id=screening1.theater_id, reserved=False).first()
    seat2 = Seat.query.filter_by(theater_id=screening2.theater_id, reserved=False).first()
    if seat1 and seat2:
        if not Ticket.query.filter_by(screening_id=screening1.id, user_id=user.id).first():
            ticket = Ticket(screening_id=screening1.id, user_id=user.id, ticketcategory_id=adult_category.id, seat_id=seat1.id)
            ticket2 = Ticket(screening_id=screening2.id, user_id=user.id, ticketcategory_id=student_category.id, seat_id=seat2.id)
            db.session.add_all([ticket, ticket2])
            seat1.reserved = True
            seat2.reserved = True
            db.session.commit()

    order = Order.query.filter_by(payment_status="Pending").first()
    ticket1 = Ticket.query.filter_by(screening_id=screening1.id).first()
    ticket2 = Ticket.query.filter_by(screening_id=screening2.id).first()
    if ticket1 and ticket2:
        if not TicketOrder.query.filter_by(ticket_id=ticket1.id).first():
            order.tickets.append(TicketOrder(ticket_id=ticket1.id, ticket_status="aktív"))
            order.tickets.append(TicketOrder(ticket_id=ticket2.id, ticket_status="aktív"))
            db.session.commit()

    print("Inicializáció kész.")
except Exception as e:
    db.session.rollback()
    print(f"Hiba történt: {e}")
    raise