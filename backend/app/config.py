# # app/config.py
# import os

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
#     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "superjwtsecret")
    
#     # Email
#     MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
#     MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
#     MAIL_USE_TLS = True
#     MAIL_USE_SSL = False
#     MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
#     MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
#     MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")


