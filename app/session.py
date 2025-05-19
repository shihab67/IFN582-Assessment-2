from flask import session


def set_user_session(user):
    session["user"] = user


def get_user_session():
    return session.get("user")


def clear_user_session():
    session.pop("user", None)
