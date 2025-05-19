from .db import db
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash


def get_users():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users


def get_user_by_email(email):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user


def create_user(form):
    password_hash = generate_password_hash(form.password.data)
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, phone_number, password) VALUES (%s, %s, %s, %s, %s)",
        (
            form.first_name.data,
            form.last_name.data,
            form.email.data,
            form.phone_number.data,
            password_hash,
        ),
    )
    db.connection.commit()
    cursor.close()
    return get_user_by_email(form.email.data)

def get_user_by_id(user_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_items():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    return items
