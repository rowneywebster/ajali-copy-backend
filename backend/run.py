# # run.py
# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

from app import create_app, db
from flask_migrate import upgrade

app = create_app()

# Run migrations at startup
with app.app_context():
    upgrade()

if __name__ == "__main__":
    app.run()

