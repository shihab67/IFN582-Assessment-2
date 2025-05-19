from flask import Blueprint
from app.decorators import login_required, admin_required

from .controllers.home_controller import index
from .controllers.login_controller import authenticate_user, logout_user
from .controllers.register_controller import register_user
from .controllers.dashboard_controller import show_dashboard

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def home():
    return index()


@main.route("/login", methods=["GET", "POST"])
def login():
    return authenticate_user()


@main.route("/register", methods=["GET", "POST"])
def register():
    return register_user()


@main.route("/dashboard", methods=["GET"])
@login_required
@admin_required
def dashboard():
    return show_dashboard()


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    return logout_user()
