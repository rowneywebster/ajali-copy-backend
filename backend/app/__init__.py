# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, mail

# Import Blueprints
from .routes.auth import auth_bp
from .routes.incidents import incidents_bp
from .routes.media import media_bp
from .routes.comments import comments_bp
from .routes.admin import admin_bp
from .routes.users import users_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(users_bp)

    return app
