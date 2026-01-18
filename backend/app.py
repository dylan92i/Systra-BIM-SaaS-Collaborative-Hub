import os
from flask import Flask, session
from config import Config
from models import db
from api_controllers import auth_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.secret_key = "lêLh1&42U¨°J43I4vm%µ£KzKfo4323èG&432hÿA"

    # Détection de l'environnement
    IS_PROD = os.environ.get("FLASK_ENV") == "production"

    # Session configuration : secure en prod
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=IS_PROD,  # True en prod (https), False en dev
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=3600
    )

    # Définition des origines autorisées selon l'environnement
    frontend_origins = [
        "https://systra.jeremieondzaghe.fr"
    ]
    if not IS_PROD:
        frontend_origins.append("http://localhost:5173")

    CORS(
        app,
        resources={r"/*": {"origins": frontend_origins}},
        supports_credentials=True,
        expose_headers=["Set-Cookie"],
        allow_headers=["Content-Type", "Authorization", "Set-Cookie"]
    )

    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
