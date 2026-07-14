from flask import Blueprint, request, jsonify

from app import db
from app.api.utils import (
    api_error,
    api_response,
    delete_trek_image,
    parse_date,
    parse_int,
    request_data,
    require_role,
    save_trek_image,
    serialize_booking,
    serialize_staff,
    serialize_trek,
    serialize_user,
)
from app.models.booking import Booking
from app.models.staff import Staff
from app.models.trek import Trek
from app.models.user import User

from app.cache import cache


admin_api = Blueprint("admin_api", __name__)


@cache.cached(timeout=300)
@admin_api.route("/dashboard", methods=["GET"])
@require_role("admin")
def dashboard():
    
    trek_status_data = [
        {"status": "Open", "count": Trek.query.filter_by(status="Open").count()},
        {"status": "Closed", "count": Trek.query.filter_by(status="Closed").count()},
        {"status": "Ongoing", "count": Trek.query.filter_by(status="Ongoing").count()},
        {"status": "Completed", "count": Trek.query.filter_by(status="Completed").count()},
    ]

    return api_response(
        {
            "total_treks": Trek.query.count(),
            "total_staff": Staff.query.count(),
            "total_trekkers": User.query.filter_by(role="trekker").count(),
            "total_bookings": Booking.query.count(),
            "trek_status_data": trek_status_data,
        }
    )

@cache.cached(timeout=300)
@admin_api.route("/treks", methods=["GET"])
@require_role("admin")
def manage_treks():
    query = request.args.get("query", "").strip()
    treks_query = Trek.query.filter(Trek.status != "Completed")

    if query:
        treks_query = treks_query.filter(Trek.name.ilike(f"%{query}%"))

    treks_list = treks_query.order_by(Trek.start_date.asc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})


@cache.cached(timeout=300)
@admin_api.route("/trekking-history", methods=["GET"])
@require_role("admin")
def trekking_history():
    query = request.args.get("query", "").strip()
    treks_query = Trek.query.filter_by(status="Completed")

    if query:
        treks_query = treks_query.filter(Trek.name.ilike(f"%{query}%"))

    treks_list = treks_query.order_by(Trek.start_date.desc()).all()
    return api_response({"treks": [serialize_trek(trek) for trek in treks_list]})


def trek_payload(existing_id=None):
    data = request_data()
    required_fields = ["name", "location", "difficulty", "duration", "slots", "start_date", "end_date"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}!")

    name = data.get("name").strip()
    existing = Trek.query.filter(Trek.name == name)
    if existing_id is not None:
        existing = existing.filter(Trek.id != existing_id)
    if existing.first():
        raise ValueError("Trek already exists!")

    slots = parse_int(data.get("slots"), "Slots", minimum=0)
    start_date = parse_date(data.get("start_date"), "Start date")
    end_date = parse_date(data.get("end_date"), "End date")
    if end_date < start_date:
        raise ValueError("End date cannot be before start date!")

    difficulty = data.get("difficulty")
    if difficulty not in {"Easy", "Moderate", "Hard"}:
        raise ValueError("Difficulty must be Easy, Moderate, or Hard!")

    return {
        "name": name,
        "location": data.get("location").strip(),
        "difficulty": difficulty,
        "duration": data.get("duration").strip(),
        "slots": slots,
        "start_date": start_date,
        "end_date": end_date,
    }


@admin_api.route("/add-trek", methods=["POST"])
@require_role("admin")
def add_trek():
    try:
        payload = trek_payload()
        image_name = save_trek_image(request.files.get("image"))
    except ValueError as exc:
        return api_error(str(exc), 400)

    trek = Trek(**payload, image=image_name)
    db.session.add(trek)
    db.session.commit()

    cache.clear()

    return api_response({"trek": serialize_trek(trek)}, f'Trek "{trek.name}" added successfully!')


@cache.cached(timeout=300)
@admin_api.route("/trek-details/<int:trek_id>", methods=["GET"])
@require_role("admin")
def trek_details(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    return api_response({"trek": serialize_trek(trek)})


@admin_api.route("/edit-trek/<int:trek_id>", methods=["PUT", "POST"])
@require_role("admin")
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    try:
        payload = trek_payload(existing_id=trek.id)
        new_image = save_trek_image(request.files.get("image"))
    except ValueError as exc:
        return api_error(str(exc), 400)

    for key, value in payload.items():
        setattr(trek, key, value)

    if new_image:
        delete_trek_image(trek.image)
        trek.image = new_image

    db.session.commit()

    cache.clear()

    return api_response({"trek": serialize_trek(trek)}, f'Trek "{trek.name}" updated successfully!')


@admin_api.route("/delete-trek/<int:trek_id>", methods=["POST"])
@require_role("admin")
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    name = trek.name
    delete_trek_image(trek.image)
    db.session.delete(trek)
    db.session.commit()

    cache.clear()

    return api_response(message=f'Trek "{name}" deleted successfully!')


@cache.cached(timeout=300)
@admin_api.route("/staff", methods=["GET"])
@require_role("admin")
def manage_staff():
    query = request.args.get("query", "").strip()

    staff_query = Staff.query
    if query:
        staff_query = staff_query.filter(Staff.full_name.ilike(f"%{query}%"))

    return api_response(
        {
            "staff": [serialize_staff(staff) for staff in staff_query.all()],
        }
    )


@admin_api.route("/create-staff", methods=["POST"])
@require_role("admin")
def create_staff():

    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip()
    full_name = (data.get("full_name") or "").strip()
    contact = (data.get("contact") or "").strip()
    password = data.get("password") or ""
    role = data.get("role") or "trekker"

    if not email or "@" not in email:
        return jsonify({
            "success": False,
            "message": "Not a valid email!"
        }), 400

    if not full_name:
        return jsonify({
            "success": False,
            "message": "Full name is required!"
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters!"
        }), 400

    if role not in ["staff"]:
        return jsonify({
            "success": False,
            "message": "Invalid role selected!"
        }), 400

    if contact and not (10 <= len(contact) <= 15):
        return jsonify({
            "success": False,
            "message": "Contact must be between 10 and 15 characters!"
        }), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists! Please Login!"
        }), 409

    # Create User
    user = User(
        email=email,
        full_name=full_name,
        contact=contact,
        role=role
    )

    user.set_password(password)

    db.session.add(user)

    # Flush to get user.id without committing
    db.session.flush()


    staff = Staff(
        email=email,
        full_name=full_name,
        contact=contact,
        user_id=user.id
    )

    db.session.add(staff)

    db.session.commit()

    cache.clear()

    return jsonify({
        "success": True,
        "message": "Staff created successfully!"
    })


@admin_api.route("/staff/<int:staff_id>/status", methods=["POST"])
@require_role("admin")
def change_staff_status(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    user = User.query.get_or_404(staff.user_id)
    data = request_data()
    status = data.get("status")
    if status not in {"Active", "Blacklisted"}:
        return api_error("Invalid staff status!", 400)

    staff.status = status
    user.status = status
    db.session.commit()

    cache.clear()

    return api_response({"staff": serialize_staff(staff)}, f'Staff account "{status}" successfully!')


@cache.cached(timeout=300)
@admin_api.route("/trek/<int:trek_id>/staff", methods=["GET"])
@require_role("admin")
def assignable_staff(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    query = request.args.get("query", "").strip()
    staff_query = Staff.query.filter_by(status="Active")

    if query:
        staff_query = staff_query.filter(Staff.full_name.ilike(f"%{query}%"))

    return api_response(
        {
            "trek": serialize_trek(trek),
            "staff": [serialize_staff(staff) for staff in staff_query.all()],
        }
    )


@admin_api.route("/trek/<int:trek_id>/assign-staff/<int:staff_id>", methods=["POST"])
@require_role("admin")
def assign_staff(trek_id, staff_id):
    trek = Trek.query.get_or_404(trek_id)
    staff = Staff.query.get_or_404(staff_id)
    if staff.status != "Active":
        return api_error("Only active staff can be assigned!", 400)

    trek.assigned_staff_id = staff.id
    db.session.commit()

    cache.clear()

    return api_response({"trek": serialize_trek(trek)}, f'Staff "{staff.full_name}" assigned to "{trek.name}" successfully!')


@admin_api.route("/trek/<int:trek_id>/remove-staff/<int:staff_id>", methods=["POST"])
@require_role("admin")
def remove_staff(trek_id, staff_id):
    trek = Trek.query.get_or_404(trek_id)
    staff = Staff.query.get_or_404(staff_id)

    if trek.assigned_staff_id != staff_id:
        return api_error("This staff member is not assigned to this trek!", 400)

    trek.assigned_staff_id = None
    db.session.commit()

    cache.clear()

    return api_response({"trek": serialize_trek(trek)}, f'Staff "{staff.full_name}" removed from "{trek.name}" successfully!')


@cache.cached(timeout=300)
@admin_api.route("/bookings", methods=["GET"])
@require_role("admin")
def bookings():
    all_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return api_response({"bookings": [serialize_booking(booking) for booking in all_bookings]})


@cache.cached(timeout=300)
@admin_api.route("/users", methods=["GET"])
@require_role("admin")
def users():
    query = request.args.get("query", "").strip()
    users_query = User.query.filter_by(role="trekker")
    if query:
        users_query = users_query.filter(User.full_name.ilike(f"%{query}%"))

    return api_response({"users": [serialize_user(user) for user in users_query.all()]})


@admin_api.route("/user/<int:user_id>/change-status", methods=["POST"])
@require_role("admin")
def change_user_status(user_id):
    user = User.query.get_or_404(user_id)
    data = request_data()
    status = data.get("status")
    if user.role == "admin":
        return api_error("Admin users cannot be blacklisted!", 400)
    if user.role == "staff":
        staff = Staff.query.filter_by(user_id=user.id).first()
        staff.status = status
    if status not in {"Active", "Blacklisted"}:
        return api_error("Invalid user status!", 400)

    user.status = status
    db.session.commit()

    cache.clear()
    
    return api_response({"user": serialize_user(user)}, f'User account "{status}" successfully!')
