from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.api.utils import api_error, api_response, request_data, serialize_user, validate_profile_payload
from app.models.user import User
from app.models.staff import Staff

from app.cache import cache


auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/login", methods=["POST"])
def login():

    if current_user.is_authenticated:
        return jsonify({
            "success": True,
            "message": "You are already logged in!"
        }), 200


    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required!"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password!"
        }), 401

    if not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password!"
        }), 401

    if user.status == "Blacklisted":
        return jsonify({
            "success": False,
            "message": "Your account is blacklisted by admin!"
        }), 403

    if user.status != "Active":
        return jsonify({
            "success": False,
            "message": "Your account is inactive!"
        }), 403

    if user.role == "admin":

        login_user(user)
        return jsonify({
                        "success": True,
                        "message": "Admin logged in successfully!",
                        "user": serialize_user(user)
                    })

    elif user.role == "staff":

        staff = Staff.query.filter_by(user_id=user.id).first()

        if not staff:

            return jsonify({
                "success": False,
                "message": "Staff account not found!"
            }), 403

        if staff.status == "Active":

            login_user(user)
            return jsonify({
                            "success": True,
                            "message": "Staff logged in successfully!",
                            "user": serialize_user(user)
                        })
        
        elif staff.status == "Blacklisted":

            return jsonify({
                "success": False,
                "message": "Your staff account is blacklisted by admin!"
            }), 403

    else:

        login_user(user)
        return jsonify({
                        "success": True,
                        "message": "Trekker logged in successfully!",
                        "user": serialize_user(user)
                    })



@auth_api.route("/register", methods=["POST"])
def register():

    if current_user.is_authenticated:
        return jsonify({
            "success": True,
            "message": "You are already registered!"
        }), 200

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

    if role not in ["trekker"]:
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

    # Create Staff record if role is staff
    if role == "staff":

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
        "message": f'{role.capitalize()} registration successful!'
    })


@cache.cached(timeout=300)
@auth_api.route("/user-profile", methods=["GET"])
def user_profile():
    if not current_user.is_authenticated:
        return api_error("Not authenticated!", 401)

    return api_response({"user": serialize_user(current_user)})


@auth_api.route("/update-profile", methods=["PUT", "POST"])
def update_profile():
    if not current_user.is_authenticated:
        return api_error("Please login to continue!", 401)

    data = request_data()
    try:
        email, full_name, contact = validate_profile_payload(data)
    except ValueError as exc:
        return api_error(str(exc), 400)

    existing = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing:
        return api_error("Email already exists!", 409)

    current_user.email = email
    current_user.full_name = full_name
    current_user.contact = contact

    if current_user.role == "staff":
        staff = Staff.query.filter_by(user_id=current_user.id).first()
        if staff:
            staff.email = email
            staff.full_name = full_name
            staff.contact = contact

    db.session.commit()

    cache.clear()

    return api_response({"user": serialize_user(current_user)}, "Your details updated successfully!")


@auth_api.route("/change-password", methods=["POST"])
def change_password():
    if not current_user.is_authenticated:
        return api_error("Please login to continue!", 401)

    data = request_data()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    if len(password) < 8:
        return api_error("Password must be at least 8 characters!", 400)
    if password != confirm_password:
        return api_error("Passwords do not match!", 400)

    current_user.set_password(password)
    db.session.commit()

    cache.clear()
    
    return api_response(message="Your password changed successfully!")


@auth_api.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    return jsonify({
        "success": True,
        "message": "Logout successful!"
    })
