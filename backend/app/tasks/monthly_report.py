from collections import Counter
from datetime import date

from flask import render_template
from flask_mail import Message

from celery_worker import celery
from app import create_app, mail
from app.models.booking import Booking
from app.models.trek import Trek
from app.models.staff import Staff
from app.models.user import User

app = create_app()


@celery.task
def send_monthly_report():

    with app.app_context():

        today = date.today()

        # Treks conducted this month
        treks = [
            trek for trek in Trek.query.all()
            if trek.start_date.month == today.month
            and trek.start_date.year == today.year
        ]

        total_treks = len(treks)

        trek_ids = [trek.id for trek in treks]

        bookings = (
            Booking.query
            .filter(Booking.status != "Cancelled")
            .all()
        )

        monthly_bookings = [
            booking for booking in bookings
            if booking.trek_id in trek_ids
        ]

        total_participants = len(monthly_bookings)

        trek_counter = Counter()

        for booking in monthly_bookings:
            trek_counter[booking.trek.name] += 1

        trek_statistics = []

        for trek in treks:

            participants = trek_counter.get(trek.name, 0)

            trek_statistics.append({
                "name": trek.name,
                "location": trek.location,
                "duration": trek.duration,
                "start_date": trek.start_date,
                "end_date": trek.end_date,
                "assigned_staff": trek.staff.full_name if trek.staff else 'Not Assigned',
                "participants": participants
            })

        top_three = trek_counter.most_common(3)

        if trek_counter:
            popular_trek = top_three[0][0]
            booking_count = top_three[0][1]
        else:
            popular_trek = "N/A"
            booking_count = 0
            
        admin = User.query.filter_by(role="admin").first()

        if not admin:
            return "Admin not found."

        msg = Message(
            subject=f"Monthly Trekking Report - {today.strftime('%B %Y')}",
            recipients=[admin.email]
        )

        msg.html = render_template(
                        "emails/monthly_report.html",
                        month=today.strftime("%B %Y"),
                        total_treks=total_treks,
                        total_participants=total_participants,
                        popular_trek=popular_trek,
                        booking_count=booking_count,
                        trek_statistics=trek_statistics,
                        top_three=top_three
                        )

        mail.send(msg)

        return "Monthly report sent successfully."