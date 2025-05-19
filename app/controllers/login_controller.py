from flask import render_template, redirect, url_for, flash, request, session
from ..session import get_user_session
from ..models import get_user_by_email
from werkzeug.security import check_password_hash
from ..forms import LoginForm
from ..session import set_user_session


def authenticate_user():
    try:
        user = get_user_session()
        if user:
            flash("You are already logged in", "info")
            return redirect(url_for("main.home"))

        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = get_user_by_email(email)
            if user and check_password_hash(user["password"], password):
                set_user_session(user)
                flash("Login successful!", "success")

                if user["role"] == "admin":
                    return redirect(url_for("main.dashboard"))
                else:
                    return redirect(url_for("main.home"))
            else:
                flash("Invalid email or password.", "danger")

        return render_template("login.html", form=form)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(request.referrer)


def logout_user():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect(url_for("main.home"))
