from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.extensions import db, mail
from app.models import User
from flask_mail import Message

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")


# ---------------------
# Token helpers
# ---------------------
def generate_token(email):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="password-reset-salt")


def verify_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None


# ---------------------
# Signup
# ---------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    user = User(name=name, email=email, phone=phone)
    user.password = password
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


# ---------------------
# Login
# ---------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # 🔑 Cast user.id to str
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "points": user.points
        }
    })


# ---------------------
# Current logged-in user
# ---------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())  # 🔑 Cast back to int
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "points": user.points
    })


# ---------------------
# Refresh token
# ---------------------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())  # 🔑 Cast back to int
    access_token = create_access_token(identity=str(user_id))
    return jsonify({"access_token": access_token})


# ---------------------
# Password reset request
# ---------------------
@auth_bp.route("/password-reset-request", methods=["POST"])
def password_reset_request():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Email not registered"}), 404

    token = generate_token(email)
    reset_url = url_for("auth_bp.password_reset", token=token, _external=True)

    msg = Message(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Hi {user.name},\n\nClick the link to reset your password: {reset_url}\n\nIf you did not request this, ignore this email."
    )
    mail.send(msg)
    return jsonify({"msg": "Password reset email sent"}), 200


# ---------------------
# Password reset
# ---------------------
@auth_bp.route("/password-reset/<token>", methods=["POST"])
def password_reset(token):
    data = request.get_json()
    new_password = data.get("password")

    email = verify_token(token)
    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.password = new_password
    db.session.commit()
    return jsonify({"msg": "Password updated successfully"})



@auth_bp.route("/seed-admin", methods=["POST"])
def seed_admin():
    from app.models import User
    from app.extensions import db, bcrypt

    # Check if an admin already exists
    if User.query.filter_by(email="superadmin@example.com").first():
        return {"message": "⚠️ Admin already exists"}, 400

    # Create admin with a secure password
    hashed_pw = bcrypt.generate_password_hash("AdminPassword123").decode("utf-8")
    admin = User(
        username="superadmin",
        email="superadmin@example.com",
        password=hashed_pw,
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()

    return {"message": "✅ Superadmin created!"}, 201

