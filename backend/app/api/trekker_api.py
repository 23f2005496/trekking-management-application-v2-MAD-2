from flask import Blueprint, request
from flask_login import current_user
from app import db
from app.api.utils import api_error, api_response, require_role, serialize_booking, serialize_trek
from app.models.booking import Booking
from app.models.trek import Trek

import os
from app.cache import cache
from app.tasks.export_csv import export_bookings
from celery_worker import celery
from flask import current_app, send_from_directory


trekker_api = Blueprint("trekker_api", __name__)


@cache.cached(timeout=300)
@trekker_api.route("/dashboard", methods=["GET"])
@require_role("trekker")
def dashboard():
    upcoming_treks = (
        Trek.query.join(Booking)
        .filter(
            Booking.user_id == current_user.id,
            Booking.status == "Booked",
            Trek.id == Booking.trek_id,
            Trek.status != "Completed",
        )
        .order_by(Trek.start_date.asc())
        .all()
    )

    completed_treks = (
        Trek.query.join(Booking)
        .filter(
            Booking.user_id == current_user.id,
            Booking.status == "Completed",
            Trek.id == Booking.trek_id,
            Trek.status == "Completed",
        )
        .count()
    )

    return api_response(
        {
            "total_bookings": Booking.query.filter_by(user_id=current_user.id).count(),
            "cancelled_bookings": Booking.query.filter_by(
                user_id=current_user.id, status="Cancelled"
            ).count(),
            "completed_treks": completed_treks,
            "upcoming_treks": [serialize_trek(trek) for trek in upcoming_treks],
        }
    )


@cache.cached(timeout=300)
@trekker_api.route("/treks", methods=["GET"])
@require_role("trekker")
def get_treks():
    location = request.args.get("location", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    treks_query = Trek.query

    if location:
        treks_query = treks_query.filter(Trek.location.ilike(f"%{location}%"))
    if difficulty:
        treks_query = treks_query.filter_by(difficulty=difficulty)

    treks_list = treks_query.order_by(Trek.start_date.desc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})


@cache.cached(timeout=300)
@trekker_api.route("/trek-details/<int:trek_id>", methods=["GET"])
@require_role("trekker")
def trek_details(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    booking = (
        Booking.query.filter_by(user_id=current_user.id, trek_id=trek.id)
        .order_by(Booking.booking_date.desc()).first()
    )

    return api_response({"trek": serialize_trek(trek), "booking": serialize_booking(booking, include_user=False)})


@trekker_api.route("/trek/<int:trek_id>/book", methods=["POST"])
@require_role("trekker")
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    existing = Booking.query.filter_by(user_id=current_user.id, status="Booked", trek_id=trek.id).first()

    if existing:
        return api_error("You have already booked this trek!", 409)
    if trek.status != "Open":
        return api_error("Booking closed!", 400)
    if trek.slots <= 0:
        return api_error("No slots available!", 400)

    booking = Booking(status="Booked", user_id=current_user.id, trek_id=trek.id)
    trek.slots -= 1
    db.session.add(booking)
    db.session.commit()

    cache.clear()

    return api_response(
        {"booking": serialize_booking(booking, include_user=False), "trek": serialize_trek(trek)},
        "Trek booked successfully!")


@trekker_api.route("/booking/<int:booking_id>/cancel", methods=["POST"])
@require_role("trekker")
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        return api_error("Unauthorized action!", 403)

    trek = Trek.query.get_or_404(booking.trek_id)

    if trek.status == "Completed":
        return api_error("Cannot cancel booking for completed trek!", 400)
    if trek.status == "Ongoing":
        return api_error("Cannot cancel booking for ongoing trek!", 400)
    if booking.status == "Cancelled":
        return api_error("You already cancelled this booking!", 400)

    booking.status = "Cancelled"
    trek.slots += 1
    db.session.commit()

    cache.clear()

    return api_response(
        {"booking": serialize_booking(booking, include_user=False), "trek": serialize_trek(trek)},
        "Booking cancelled successfully!")

@cache.cached(timeout=300)
@trekker_api.route("/bookings", methods=["GET"])
@require_role("trekker")
def bookings():
    my_bookings = (
        Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    )
    return api_response({"bookings": [serialize_booking(booking, include_user=False) for booking in my_bookings]})


@cache.cached(timeout=300)
@trekker_api.route("/trekking-history", methods=["GET"])
@require_role("trekker")
def trekking_history():
    query = request.args.get("query", "").strip()
    treks_query = Trek.query.join(Booking).filter(
        Booking.user_id == current_user.id,
        Trek.id == Booking.trek_id,
        Trek.status == "Completed",
    )

    if query:
        treks_query = treks_query.filter(Trek.name.ilike(f"%{query}%"))

    treks_list = treks_query.order_by(Trek.start_date.desc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})



# For User Triggered Async Job – Export Booking History as CSV


@trekker_api.route("/export-bookings", methods=["POST"])
@require_role("trekker")
def export_booking_history():

    task = export_bookings.delay(current_user.id)

    return api_response({
        "message": "Generating CSV File.....",
        "task_id": task.id
    })



@trekker_api.route("/export-status/<task_id>", methods=["GET"])
@require_role("trekker")
def export_status(task_id):

    task = celery.AsyncResult(task_id)

    response = {
        "status": task.status
    }

    if task.status == "SUCCESS":
        response["filename"] = task.result
        response["message"] = "Your file is ready. Click on save!"

    return api_response(response)



@trekker_api.route("/download/<filename>", methods=["GET"])
def download_file(filename):

    project_root = os.path.abspath(
        os.path.join(current_app.root_path, "..")
    )

    export_folder = os.path.join(project_root, "exports")

    return send_from_directory(
        export_folder,
        filename,
        as_attachment=True
    )

