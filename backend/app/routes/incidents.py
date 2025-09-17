# app/routes/incidents.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Incident, Comment, Media, User

incidents_bp = Blueprint("incidents", __name__, url_prefix="/api/v1/incidents")


# ------------------------
# Create a new incident
# ------------------------
@incidents_bp.route("/", methods=["POST"])
@jwt_required()
def create_incident():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data or not all(k in data for k in ("title", "description", "latitude", "longitude")):
        return jsonify({"msg": "Missing required fields"}), 400

    incident = Incident(
        title=data["title"],
        description=data["description"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        status="pending",
        created_by=current_user_id
    )
    db.session.add(incident)
    db.session.commit()

    return jsonify({"msg": "Incident created", "id": incident.id}), 201


# ------------------------
# Get all incidents
# ------------------------
@incidents_bp.route("/", methods=["GET"])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "latitude": i.latitude,
            "longitude": i.longitude,
            "status": i.status,
            "created_by": i.created_by
        } for i in incidents
    ])


# ------------------------
# Get a single incident by ID
# ------------------------
@incidents_bp.route("/<int:incident_id>", methods=["GET"])
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return jsonify({
        "id": incident.id,
        "title": incident.title,
        "description": incident.description,
        "latitude": incident.latitude,
        "longitude": incident.longitude,
        "status": incident.status,
        "created_by": incident.created_by
    })


# ------------------------
# Get incidents belonging to the logged-in user
# ------------------------
@incidents_bp.route("/mine", methods=["GET"])
@jwt_required()
def my_incidents():
    user_id = get_jwt_identity()
    incidents = Incident.query.filter_by(created_by=user_id).all()
    return jsonify([
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "status": i.status,
            "created_by": i.created_by
        } for i in incidents
    ])


# ------------------------
# Update an incident
# ------------------------
@incidents_bp.route("/<int:incident_id>", methods=["PUT"])
@jwt_required()
def update_incident(incident_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    incident = Incident.query.get_or_404(incident_id)

    user = User.query.get(current_user_id)
    if incident.created_by != current_user_id and user.role != "admin":
        return jsonify({"msg": "Not authorized"}), 403

    # Update only provided fields
    if "title" in data:
        incident.title = data["title"]
    if "description" in data:
        incident.description = data["description"]
    if "latitude" in data:
        incident.latitude = data["latitude"]
    if "longitude" in data:
        incident.longitude = data["longitude"]
    if "status" in data:
        incident.status = data["status"]

    db.session.commit()
    return jsonify({"msg": "Incident updated"})


# ------------------------
# Delete an incident
# ------------------------
@incidents_bp.route("/<int:incident_id>", methods=["DELETE"])
@jwt_required()
def delete_incident(incident_id):
    current_user_id = get_jwt_identity()
    incident = Incident.query.get_or_404(incident_id)

    user = User.query.get(current_user_id)
    if incident.created_by != current_user_id and user.role != "admin":
        return jsonify({"msg": "Not authorized"}), 403

    db.session.delete(incident)
    db.session.commit()
    return jsonify({"msg": "Incident deleted"})


# ------------------------
# Add a comment to an incident
# ------------------------
@incidents_bp.route("/<int:incident_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(incident_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data or "text" not in data:
        return jsonify({"msg": "Missing comment text"}), 400

    comment = Comment(
        text=data["text"],
        incident_id=incident_id,
        created_by=current_user_id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"msg": "Comment added", "id": comment.id}), 201


# ------------------------
# Upload media to an incident
# ------------------------
@incidents_bp.route("/<int:incident_id>/media", methods=["POST"])
@jwt_required()
def upload_media(incident_id):
    if "file" not in request.files:
        return jsonify({"msg": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"msg": "Empty filename"}), 400

    filename = file.filename
    file_url = f"/uploads/{filename}"

    current_user_id = get_jwt_identity()
    media = Media(
        filename=filename,
        file_url=file_url,
        incident_id=incident_id,
        uploaded_by=current_user_id
    )
    db.session.add(media)
    db.session.commit()

    return jsonify({"msg": "Media uploaded", "id": media.id, "file_url": file_url}), 201
