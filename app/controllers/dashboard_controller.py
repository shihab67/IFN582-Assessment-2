from flask import render_template, redirect, url_for, flash
from ..session import get_user_session
from ..forms import LoginForm
from ..session import set_user_session


def show_dashboard():
    return render_template("dashboard/dashboard.html")
