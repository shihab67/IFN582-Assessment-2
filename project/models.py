from .db import db
import MySQLdb.cursors
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


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
    password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
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


def get_items(category=None, search=None):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT items.*, categories.name AS category_name
        FROM items
        JOIN categories ON items.category_id = categories.id
        WHERE items.name LIKE %s
    """
    params = [f'%{search}%']

    if category != 'all':
        query += " AND categories.name = %s"
        params.append(category)

    cursor.execute(query, params)
    items = cursor.fetchall()
    cursor.close()
    return items


def get_item(item_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT items.*, categories.name AS category_name
        FROM items
        JOIN categories ON items.category_id = categories.id
        WHERE items.id = %s
    """,
        (item_id,),
    )
    product = cursor.fetchone()
    cursor.close()
    return product


def get_categories():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM categories ORDER BY name ASC")
    categories = cursor.fetchall()
    cursor.close()
    return categories
