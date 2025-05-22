from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page!", "warning")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user"] and session["user"]["role"] != "admin":
            flash("You don't have permission to perform this operation!", "danger")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function
