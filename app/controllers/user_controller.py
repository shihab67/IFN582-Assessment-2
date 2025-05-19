from flask import session, redirect, url_for, flash
from models import get_users
import hashlib

# def login_user(email, password):
#     user = get_user_by_email(email)
#     if not user:
#         flash("User not found", "danger")
#         return redirect(url_for("login"))

#     password_hash = hashlib.sha256(password.encode()).hexdigest()
#     if user[2] != password_hash:
#         flash("Incorrect password", "danger")
#         return redirect(url_for("login"))

#     session["user_id"] = user[0]
#     flash("Logged in successfully", "success")
#     return redirect(url_for("dashboard"))
