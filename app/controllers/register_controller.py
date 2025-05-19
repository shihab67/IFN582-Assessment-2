from flask import render_template, redirect, url_for, flash, request
from ..session import get_user_session
from ..models import get_user_by_email, create_user
from ..forms import RegisterForm
from ..session import set_user_session


def register_user():
    user = get_user_session()
    if user:
        flash("You are already logged in", "info")
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = get_user_by_email(email)
        if user:
            flash("Email already exists", "danger")
            return redirect(request.referrer)
        else:
            user = create_user(form)
            if not user:
                flash("Something went wrong. Please try again!", "danger")
                return redirect(request.referrer)
            else:
                flash("Registration successful. You can now login!", "success")
                return redirect(url_for("main.login"))
            

    return render_template("register.html", form=form)
