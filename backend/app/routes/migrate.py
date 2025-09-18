from flask import Blueprint, jsonify
from flask_migrate import upgrade
import os

migrate_bp = Blueprint("migrate", __name__, url_prefix="/migrate")

@migrate_bp.route("/upgrade", methods=["GET"])
def run_upgrade():
    try:
        upgrade()
        return jsonify({"msg": "Database upgraded!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
