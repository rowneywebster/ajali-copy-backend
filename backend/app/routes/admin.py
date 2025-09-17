# app/routes/admin.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, mail
from app.models import Incident, User
from flask_mail import Message

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/v1/admin")

# ---------------------
# Admin check decorator
# ---------------------
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# ---------------------
# List all incidents (with optional status filter)
# GET /api/v1/admin/incidents
# ---------------------
@admin_bp.route("/incidents", methods=["GET"])
@admin_required
def list_all_incidents():
    status_filter = request.args.get("status")
    query = Incident.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    incidents = query.all()
    result = [
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "status": i.status,
            "created_by": i.created_by,
            "created_at": i.created_at
        } for i in incidents
    ]
    return jsonify(result)

# ---------------------
# Update incident status
# PATCH /api/v1/admin/incidents/<id>/status
# ---------------------
@admin_bp.route("/incidents/<int:id>/status", methods=["PATCH"])
@admin_required
def update_incident_status(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["investigating", "resolved", "rejected"]:
        return jsonify({"msg": "Invalid status"}), 400

    incident.status = new_status
    db.session.commit()

    # Notify reporter via email
    reporter = User.query.get(incident.created_by)
    if reporter and reporter.email:
        try:
            msg = Message(
                subject=f"Incident #{incident.id} Status Updated",
                recipients=[reporter.email],
                body=f"Hi {reporter.name},\n\nYour incident '{incident.title}' status has been updated to '{new_status}'."
            )
            mail.send(msg)
        except Exception as e:
            print(f"Email send failed: {e}")

    return jsonify({"msg": f"Incident status updated to {new_status}"})
