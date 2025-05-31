from .db import db
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from flask import session

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
    """

    filters = []
    params = []

    if search:
        filters.append("items.name LIKE %s")
        params.append(f"%{search}%")

    if category and category != "all":
        filters.append("categories.name = %s")
        params.append(category)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY items.id DESC"

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


def get_orders(user_id=None, status=None):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    query = "SELECT * FROM orders"
    conditions = []
    params = []

    if not session.get("is_admin") and user_id is not None:
        conditions.append("user_id = %s")
        params.append(user_id)

    if status is not None:
        conditions.append("status = %s")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    orders = cursor.fetchall()

    for order in orders:
        cursor.execute(
            """
            SELECT 
                oi.id AS order_item_id,
                oi.order_id,
                oi.item_id,
                oi.quantity,
                oi.price,
                
                i.id AS item_id,
                i.name AS item_name,
                i.description AS item_description,
                i.image AS item_image,
                i.price AS item_price,

                c.id AS category_id,
                c.name AS category_name

            FROM order_items oi
            JOIN items i ON oi.item_id = i.id
            JOIN categories c ON i.category_id = c.id
            WHERE oi.order_id = %s
            """,
            (order["id"],),
        )
        order["items"] = cursor.fetchall()

    cursor.close()
    return orders


def update_order(order_id, status):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    if status.lower() == "delivered":
        delivered_at = datetime.now(timezone.utc)
        cursor.execute(
            "UPDATE orders SET status = %s, delivered_at = %s WHERE id = %s",
            (status, delivered_at, order_id),
        )
    else:
        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s", (status, order_id)
        )

    db.connection.commit()
    cursor.close()
    return


def create_order(full_name, address, phone, delivery_option, total, user_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO orders (user_id, full_name, address, phone, order_date, delivery_option, total) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            user_id,
            full_name,
            address,
            phone,
            datetime.now(timezone.utc),
            delivery_option,
            total,
        ),
    )
    db.connection.commit()
    order_id = cursor.lastrowid
    cursor.close()
    return order_id


def create_order_items(order_id, item_id, quantity, price):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
        (order_id, item_id, quantity, price),
    )
    db.connection.commit()
    cursor.close()
    return


def create_item(name, price, description, category, image):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO items (name, price, description, category_id, image) VALUES (%s, %s, %s, %s, %s)",
        (
            name,
            price,
            description,
            category,
            image,
        ),
    )
    db.connection.commit()
    cursor.close()
    return


def create_category(name, image):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "INSERT INTO categories (name, image) VALUES (%s, %s)",
        (name, image),
    )
    db.connection.commit()
    cursor.close()
    return


def get_categories():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM categories ORDER BY name ASC")
    categories = cursor.fetchall()
    cursor.close()
    return categories


def get_category(category_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()
    cursor.close()
    return category


def update_item(item_id, name, price, description, category, image):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "UPDATE items SET name = %s, price = %s, description = %s, category_id = %s, image = %s WHERE id = %s",
        (
            name,
            price,
            description,
            category,
            image,
            item_id,
        ),
    )
    db.connection.commit()
    cursor.close()
    return


def delete_item(item_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.connection.commit()
    cursor.close()
    return


def delete_category(category_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    db.connection.commit()
    cursor.close()
    return


def update_category(category_id, name, image):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "UPDATE categories SET name = %s , image = %s WHERE id = %s",
        (
            name,
            image,
            category_id,
        ),
    )
    db.connection.commit()
    cursor.close()
    return


def check_category_exists_in_products(category_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM items WHERE category_id = %s", (category_id,))
    product = cursor.fetchone()
    cursor.close()
    return product


def check_product_exists_in_orders(item_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM order_items WHERE item_id = %s", (item_id,))
    product = cursor.fetchone()
    cursor.close()
    return product
