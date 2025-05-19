from flask import Flask
from .db import db
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5 as Bootstrap
from .views import main
from dotenv import load_dotenv
import os

csrf = CSRFProtect()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

    Bootstrap(app)
    csrf.init_app(app)
    db.init_app(app)

    app.register_blueprint(main)

    return app
