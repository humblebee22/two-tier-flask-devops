from flask import Flask
from app.config import Config
from app.db import init_db
from app.routes import bp as tasks_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure the tasks table exists before the app starts serving requests
    init_db()

    app.register_blueprint(tasks_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
