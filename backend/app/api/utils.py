import os
from datetime import datetime
from functools import wraps

from flask import current_app, jsonify, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.models.booking import Booking

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}


def api_response(data=None, message=None, status=200, success=True):
    payload = {"success": success}
    if message is not None:
        payload["message"] = message
    if data:
        payload.update(data)
    return jsonify(payload), status


def api_error(message, status=400):
    return api_response(message=message, status=status, success=False)


def require_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return api_error("Please login to continue!", 401)
            if roles and current_user.role not in roles:
                return api_error("You don't have permission to perform this action!", 403)
            return func(*args, **kwargs)

        return wrapped

    return decorator


def request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def parse_int(value, field_name, minimum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number!")
    if minimum is not None and parsed < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}!")
    return parsed


def parse_date(value, field_name):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid date!")


def date_label(value):
    return value.strftime("%d %b %Y") if value else None


def datetime_label(value):
    return value.strftime("%d %b %Y, %I:%M %p") if value else None


def image_url(filename):
    image_name = filename or "no_image.jpg"
    return url_for("static", filename=f"images/{image_name}", _external=True)


def serialize_user(user):
    if user is None:
        return None
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "contact": user.contact,
        "status": user.status,
        "role": user.role,
    }


def serialize_staff(staff):
    if staff is None:
        return None
    return {
        "id": staff.id,
        "email": staff.email,
        "full_name": staff.full_name,
        "contact": staff.contact,
        "status": staff.status,
        "user_id": staff.user_id,
    }


def serialize_trek(trek, include_counts=True):
    if trek is None:
        return None
    data = {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "slots": trek.slots,
        "start_date": trek.start_date.isoformat() if trek.start_date else None,
        "end_date": trek.end_date.isoformat() if trek.end_date else None,
        "start_date_label": date_label(trek.start_date),
        "end_date_label": date_label(trek.end_date),
        "status": trek.status,
        "image": trek.image,
        "image_url": image_url(trek.image),
        "assigned_staff_id": trek.assigned_staff_id,
        "staff": serialize_staff(trek.staff),
    }
    if include_counts:
        data["participants"] = trek.bookings.filter(
            Booking.status.in_(["Booked", "Completed"])
        ).count()
    return data


def serialize_booking(booking, include_user=True, include_trek=True):
    if booking is None:
        return None
    data = {
        "id": booking.id,
        "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
        "booking_date_label": datetime_label(booking.booking_date),
        "status": booking.status,
        "user_id": booking.user_id,
        "trek_id": booking.trek_id,
    }
    if include_user:
        data["user"] = serialize_user(booking.user)
    if include_trek:
        data["trek"] = serialize_trek(booking.trek, include_counts=False)
    return data


def save_trek_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Only jpg, jpeg, and png images are allowed!")

    images_dir = os.path.join(current_app.root_path, "static", "images")
    os.makedirs(images_dir, exist_ok=True)
    path = os.path.join(images_dir, filename)
    file_storage.save(path)
    return filename


def delete_trek_image(filename):
    if not filename:
        return
    path = os.path.join(current_app.root_path, "static", "images", filename)
    if os.path.exists(path):
        os.remove(path)


def validate_profile_payload(data):
    email = (data.get("email") or "").strip()
    full_name = (data.get("full_name") or "").strip()
    contact = (data.get("contact") or "").strip()

    if not email or "@" not in email:
        raise ValueError("A valid email is required!")
    if not full_name:
        raise ValueError("Full name is required!")
    if contact and not (10 <= len(contact) <= 15):
        raise ValueError("Contact must be between 10 and 15 characters!")

    return email, full_name, contact
