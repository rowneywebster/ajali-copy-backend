# app/routes/comments.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Comment, Incident

comments_bp = Blueprint("comments_bp", __name__, url_prefix="/api/v1/incidents")

# ---------------------
# Add a comment to an incident
# POST /api/v1/incidents/<id>/comments
# ---------------------
@comments_bp.route("/<int:incident_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(incident_id):
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"msg": "Comment text is required"}), 400

    incident = Incident.query.get_or_404(incident_id)
    user_id = get_jwt_identity()

    comment = Comment(
        text=text,
        incident_id=incident.id,
        created_by=user_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Comment added", "comment_id": comment.id}), 201

# ---------------------
# List all comments for an incident
# GET /api/v1/incidents/<id>/comments
# ---------------------
@comments_bp.route("/<int:incident_id>/comments", methods=["GET"])
def list_comments(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    comments = Comment.query.filter_by(incident_id=incident.id).all()
    result = [
        {
            "id": c.id,
            "text": c.text,
            "created_by": c.created_by,
            "created_at": c.created_at
        } for c in comments
    ]
    return jsonify(result)
