from datetime import date

from flask_mail import Message
from flask import render_template

from app import create_app, mail
from celery_worker import celery
from app.models.booking import Booking
from app.models.trek import Trek
from app.models.user import User

app = create_app()


@celery.task
def send_daily_reminders():

    with app.app_context():

        today = date.today()

        bookings = (
            Booking.query
            .join(Trek)
            .filter(Booking.status == 'Booked', Trek.start_date >= today)
            .all()
        )

        print(f"Found {len(bookings)} bookings")

        for booking in bookings:

            user = booking.user
            trek = booking.trek

            print(f"Sending reminder to: {user.email}")

            days_left = (trek.start_date - today).days

            msg = Message(
                subject=f"🏔 Upcoming Trek Reminder - {trek.name}",
                recipients=[user.email]
            )

            # 
            msg.html = render_template(
                    "emails/daily_reminder.html",
                    user=user,
                    trek=trek,
                    days_left=days_left
                )

            mail.send(msg)
            print(f"Email sent successfully to {user.email}")

        return f"Successfully sent {len(bookings)} reminder emails."