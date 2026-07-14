from flask import Blueprint, request
from flask_login import current_user
from app import db
from app.api.utils import api_error, api_response, parse_int, request_data, require_role, serialize_booking, serialize_trek
from app.models.booking import Booking
from app.models.staff import Staff
from app.models.trek import Trek

from app.cache import cache

staff_api = Blueprint("staff_api", __name__)


def current_staff():
    return Staff.query.filter_by(user_id=current_user.id).first()


def assigned_trek_or_error(trek_id):
    staff = current_staff()
    trek = Trek.query.get_or_404(trek_id)
    if not staff or trek.assigned_staff_id != staff.id:
        return None
    return trek


@cache.cached(timeout=300)
@staff_api.route("/dashboard", methods=["GET"])
@require_role("staff")
def dashboard():
    staff = current_staff()
    if not staff:
        return api_error("Staff profile not found!", 404)

    upcoming_treks = (
        staff.assigned_treks.filter(Trek.status != "Completed").order_by(Trek.start_date.asc()).all()
    )

    trek_bookings = {}
    total_participants = 0
    for trek in upcoming_treks:
        booking_count = trek.bookings.filter_by(status="Booked").count()
        trek_bookings[trek.name] = booking_count
        total_participants += booking_count

    return api_response(
        {
            "total_assigned_treks": staff.assigned_treks.count(),
            "completed_treks": staff.assigned_treks.filter_by(status="Completed").count(),
            "upcoming_treks": [serialize_trek(trek) for trek in upcoming_treks],
            "trek_bookings": trek_bookings,
            "total_participants": total_participants,
        }
    )


@cache.cached(timeout=300)
@staff_api.route("/assigned-treks", methods=["GET"])
@require_role("staff")
def assigned_treks():
    staff = current_staff()
    if not staff:
        return api_error("Staff account not found!", 404)

    query = request.args.get("query", "").strip()
    treks_query = staff.assigned_treks.filter(Trek.status != "Completed")
    if query:
        treks_query = treks_query.filter(Trek.name.ilike(f"%{query}%"))

    treks_list = treks_query.order_by(Trek.start_date.asc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})


@cache.cached(timeout=300)
@staff_api.route("/trek-details/<int:trek_id>", methods=["GET"])
@require_role("staff")
def trek_details(trek_id):
    trek = assigned_trek_or_error(trek_id)
    if not trek:
        return api_error("You don't have permission to view this trek!", 403)

    bookings = (
        trek.bookings.filter(Booking.status.in_(["Booked", "Completed"]))
        .order_by(Booking.booking_date.desc())
        .all()
    )
    return api_response(
        {
            "trek": serialize_trek(trek),
            "bookings": [serialize_booking(booking, include_trek=False) for booking in bookings],
        }
    )


@staff_api.route("/trek/<int:trek_id>/update-slots", methods=["PUT","POST"])
@require_role("staff")
def update_slots(trek_id):
    trek = assigned_trek_or_error(trek_id)
    if not trek:
        return api_error("You don't have permission to update this trek!", 403)
    if trek.status == "Completed":
        return api_error("Cannot update slots for completed trek!", 400)

    data = request_data()
    try:
        trek.slots = parse_int(data.get("slots"), "Slots", minimum=0)
    except ValueError as exc:
        return api_error(str(exc), 400)

    db.session.commit()

    cache.clear()

    return api_response({"trek": serialize_trek(trek)}, "Slots updated successfully!")


@staff_api.route("/trek/<int:trek_id>/change-status", methods=["PUT","POST"])
@require_role("staff")
def change_trek_status(trek_id):
    trek = assigned_trek_or_error(trek_id)
    if not trek:
        return api_error("You don't have permission to update this trek!", 403)
    if trek.status == "Completed":
        return api_error("Cannot change status for completed trek!", 400)

    data = request_data()
    new_status = data.get("status")
    if new_status not in {"Open", "Closed", "Ongoing", "Completed"}:
        return api_error("Invalid trek status!", 400)

    if new_status == "Completed":
        trek.slots = 0
        for booking in trek.bookings.filter_by(status="Booked").all():
            booking.status = "Completed"

    trek.status = new_status
    db.session.commit()

    cache.clear()
    
    return api_response({"trek": serialize_trek(trek)}, "Trek status changed successfully!")


@cache.cached(timeout=300)
@staff_api.route("/trekking-history", methods=["GET"])
@require_role("staff")
def trekking_history():
    staff = current_staff()
    if not staff:
        return api_error("Staff profile not found!", 404)

    query = request.args.get("query", "").strip()
    treks_query = staff.assigned_treks.filter_by(status="Completed")
    if query:
        treks_query = treks_query.filter(Trek.name.ilike(f"%{query}%"))

    treks_list = treks_query.order_by(Trek.start_date.desc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})
