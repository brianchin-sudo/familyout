import os
import logging
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    if not os.environ.get("SERPAPI_KEY"):
        logging.warning(
            "SERPAPI_KEY is not set. Searches will return no results. "
            "Copy .env.example to .env and add your key."
        )

    from app.routes import bp
    app.register_blueprint(bp)

    return app
