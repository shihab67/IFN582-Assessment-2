from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from project.forms import ProductForm, BasketForm, CheckoutForm, RegisterForm, LoginForm
from project.models import admin_required
import MySQLdb.cursors
import re

main_bp = Blueprint('main', __name__)
mysql = MySQL()
bcrypt = Bcrypt()


def init_app(app):
    global mysql, bcrypt
    mysql = MySQL(app)
    bcrypt = Bcrypt(app)

def sanitize_input(value):
    """Sanitize input to prevent SQL injection and XSS."""
    if isinstance(value, str):
        return re.sub(r'[^\w\s-]', '', value.strip())
    return value

@main_bp.route('/')
def index():
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        category = sanitize_input(request.args.get('category', 'all'))
        search = sanitize_input(request.args.get('search', ''))
        query = "SELECT * FROM products WHERE name LIKE %s"
        params = (f'%{search}%',)
        if category != 'all':
            query += " AND category = %s"
            params = (f'%{search}%', category)
        cursor.execute(query, params)
        products = cursor.fetchall()
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = [row['category'] for row in cursor.fetchall()]
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'danger')
        return render_template('500.html'), 500
    finally:
        if cursor:
            cursor.close()
    return render_template('index.html', products=products, categories=categories, selected_category=category, search=search)

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return render_template('404.html'), 404
    except Exception as e:
        flash(f'Error loading product: {str(e)}', 'danger')
        return render_template('500.html'), 500
    finally:
        if cursor:
            cursor.close()
    return render_template('product_details.html', product=product)

@main_bp.route('/basket', methods=['GET', 'POST'])
def basket():
    form = BasketForm()
    if 'basket' not in session:
        session['basket'] = []
    basket_items = []
    total = 0
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for item in session['basket']:
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (item['product_id'],))
            product = cursor.fetchone()
            if product:
                item_total = product['price'] * item['quantity']
                basket_items.append({
                    'product_id': item['product_id'],
                    'name': product['name'],
                    'price': product['price'],
                    'image': product['image'],
                    'quantity': item['quantity'],
                    'total': item_total
                })
                total += item_total
        if form.validate_on_submit():
            product_id = int(request.form.get('product_id'))
            quantity = form.quantity.data
            if quantity < 1:
                flash('Quantity must be at least 1.', 'danger')
                return redirect(url_for('main.basket'))
            for item in session['basket']:
                if item['product_id'] == product_id:
                    item['quantity'] = quantity
                    break
            session.modified = True
            flash('Basket updated.', 'success')
            return redirect(url_for('main.basket'))
    except Exception as e:
        flash(f'Error updating basket: {str(e)}', 'danger')
        return render_template('500.html'), 500
    finally:
        if cursor:
            cursor.close()
    return render_template('basket.html', basket_items=basket_items, total=total, form=form)

@main_bp.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    try:
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            flash('Quantity must be at least 1.', 'danger')
            return redirect(url_for('main.index'))
        if 'basket' not in session:
            session['basket'] = []
        for item in session['basket']:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                session.modified = True
                flash('Item quantity updated in basket.', 'success')
                return redirect(url_for('main.basket'))
        session['basket'].append({'product_id': product_id, 'quantity': quantity})
        session.modified = True
        flash('Item added to basket.', 'success')
    except ValueError:
        flash('Invalid quantity entered.', 'danger')
    except Exception as e:
        flash(f'Error adding to basket: {str(e)}', 'danger')
    return redirect(url_for('main.basket'))

@main_bp.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    try:
        if 'basket' in session:
            session['basket'] = [item for item in session['basket'] if item['product_id'] != product_id]
            session.modified = True
            flash('Item removed from basket.', 'success')
    except Exception as e:
        flash(f'Error removing item: {str(e)}', 'danger')
    return redirect(url_for('main.basket'))

@main_bp.route('/clear_basket')
def clear_basket():
    try:
        session.pop('basket', None)
        flash('Basket cleared.', 'success')
    except Exception as e:
        flash(f'Error clearing basket: {str(e)}', 'danger')
    return redirect(url_for('main.basket'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'basket' not in session or not session['basket']:
        flash('Your basket is empty.', 'danger')
        return redirect(url_for('main.index'))
    if 'user_id' not in session:
        flash('Please log in to checkout.', 'danger')
        return redirect(url_for('main.login', next='checkout'))
    form = CheckoutForm()
    basket_items = []
    items_total = 0
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for item in session['basket']:
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (item['product_id'],))
            product = cursor.fetchone()
            if product:
                item_total = product['price'] * item['quantity']
                basket_items.append({
                    'product_id': item['product_id'],
                    'name': product['name'],
                    'price': product['price'],
                    'image': product['image'],
                    'quantity': item['quantity'],
                    'total': item_total
                })
                items_total += item_total
        delivery_costs = {'standard': 9.50, 'express': 12.50, 'green': 2.00}
        delivery_option = form.delivery_option.data if form.delivery_option.data else 'standard'
        if delivery_option not in delivery_costs:
            flash('Invalid delivery option selected.', 'danger')
            return redirect(url_for('main.checkout'))
        delivery_cost = delivery_costs.get(delivery_option, 9.50)
        total = items_total + delivery_cost
        if form.validate_on_submit():
            cursor.execute("INSERT INTO orders (user_id, full_name, address, phone, delivery_option, total) VALUES (%s, %s, %s, %s, %s, %s)",
                           (session['user_id'], sanitize_input(form.full_name.data), sanitize_input(form.address.data),
                            sanitize_input(form.phone.data), delivery_option, total))
            order_id = cursor.lastrowid
            for item in basket_items:
                cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                               (order_id, item['product_id'], item['quantity'], item['price']))
            mysql.connection.commit()
            session.pop('basket', None)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error placing order: {str(e)}', 'danger')
        return render_template('500.html'), 500
    finally:
        if cursor:
            cursor.close()
    return render_template('checkout.html', form=form, basket_items=basket_items, items_total=items_total,
                           delivery_cost=delivery_cost, total=total, delivery_costs=delivery_costs)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    cursor = None
    if form.validate_on_submit():
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            username = sanitize_input(form.username.data)
            email = sanitize_input(form.email.data)
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username or email already exists.', 'danger')
                return render_template('register.html', form=form)
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            cursor.execute("INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)",
                           (username, email, hashed_password, False))
            mysql.connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error registering user: {str(e)}', 'danger')
        finally:
            if cursor:
                cursor.close()
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    form = LoginForm()
    cursor = None
    if form.validate_on_submit():
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            username = sanitize_input(form.username.data)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                session['user_id'] = user['user_id']
                session['is_admin'] = user['is_admin']
                session.permanent = True
                flash('Logged in successfully!', 'success')
                next_page = sanitize_input(request.args.get('next', 'index'))
                return redirect(url_for(f'main.{next_page}'))
            flash('Invalid username or password.', 'danger')
        except Exception as e:
            flash(f'Error logging in: {str(e)}', 'danger')
        finally:
            if cursor:
                cursor.close()
    return render_template('login.html', form=form)

@main_bp.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        session.pop('is_admin', None)
        session.pop('basket', None)
        flash('Logged out successfully.', 'success')
    except Exception as e:
        flash(f'Error logging out: {str(e)}', 'danger')
    return redirect(url_for('main.index'))

@main_bp.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    form = ProductForm()
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if form.validate_on_submit():
            cursor.execute("INSERT INTO products (name, price, description, category, image) VALUES (%s, %s, %s, %s, %s)",
                           (sanitize_input(form.name.data), form.price.data, sanitize_input(form.description.data),
                            sanitize_input(form.category.data), sanitize_input(form.image.data)))
            mysql.connection.commit()
            flash('Product added.', 'success')
            return redirect(url_for('main.admin'))
        product_id = request.args.get('product_id', type=int)
        if product_id:
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                form.name.data = product['name']
                form.price.data = product['price']
                form.description.data = product['description']
                form.category.data = product['category']
                form.image.data = product['image']
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error managing products: {str(e)}', 'danger')
        return render_template('500.html'), 500
    finally:
        if cursor:
            cursor.close()
    return render_template('admin.html', form=form, products=products, edit_product_id=product_id)

@main_bp.route('/admin/delete/<int:product_id>')
@admin_required
def admin_delete(product_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        mysql.connection.commit()
        flash('Product deleted.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')
    finally:
        if cursor:
            cursor.close()
    return redirect(url_for('main.admin'))

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main_bp.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403