import csv
import os
from datetime import datetime

from celery_worker import celery
from app.models.booking import Booking
from app.models.trek import Trek


@celery.task
def export_bookings(user_id):

    bookings = (
        Booking.query
        .filter_by(user_id=user_id)
        .order_by(Booking.booking_date.desc())
        .all()
    )

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    export_folder = os.path.join(project_root, "exports")
    os.makedirs(export_folder, exist_ok=True)

    filename = f"booking_history_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    filepath = os.path.join(export_folder, filename)

    
    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Booking ID",
            "Trek Name",
            "Location",
            "Duration",
            "Trek Dates",
            "Booking Status",
            "Booking Date"
        ])

        for booking in bookings:

            writer.writerow([
                booking.id,
                booking.trek.name,
                booking.trek.location,
                booking.trek.duration,
                f"{booking.trek.start_date.strftime('%d-%m-%Y')} - {booking.trek.end_date.strftime('%d-%m-%Y')}",
                booking.status,
                booking.booking_date.strftime("%d-%m-%Y %I:%M %p")
            ])

    return filename