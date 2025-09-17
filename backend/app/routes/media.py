import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Media, Incident, User

media_bp = Blueprint("media_bp", __name__, url_prefix="/api/v1/media")

# Allowed extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------
# Upload media to an incident
# ---------------------
@media_bp.route("/<int:incident_id>/upload", methods=["POST"])
@jwt_required()
def upload_media(incident_id):
    user_id = get_jwt_identity()
    incident = Incident.query.get_or_404(incident_id)
    
    # Check owner/admin
    user = User.query.get(user_id)
    if incident.created_by != user_id and user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    if "file" not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"msg": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        file_url = f"/uploads/{filename}"  # For serving files later
        media = Media(
            filename=filename,
            file_url=file_url,
            incident_id=incident.id,
            uploaded_by=user_id
        )
        db.session.add(media)
        db.session.commit()
        return jsonify({"msg": "File uploaded", "media_id": media.id, "file_url": file_url})
    else:
        return jsonify({"msg": f"File type not allowed: {ALLOWED_EXTENSIONS}"}), 400

# ---------------------
# Delete media
# ---------------------
@media_bp.route("/<int:media_id>", methods=["DELETE"])
@jwt_required()
def delete_media(media_id):
    user_id = get_jwt_identity()
    media = Media.query.get_or_404(media_id)
    user = User.query.get(user_id)

    if media.uploaded_by != user_id and user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    # Remove file from filesystem
    file_path = os.path.join(current_app.root_path, "uploads", media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(media)
    db.session.commit()
    return jsonify({"msg": "Media deleted"})
