from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from flask_bcrypt import Bcrypt
from project.forms import ProductForm, BasketForm, CheckoutForm, RegisterForm, LoginForm
from project.models import (
    get_items,
    get_categories,
    get_item,
    get_user_by_email,
    create_user,
    create_order,
    create_order_items,
    create_item,
    delete_item,
)
from project.decorators import login_required, admin_required
from project.session import set_user_session, get_user_session
import re

main = Blueprint("main", __name__)
bcrypt = Bcrypt()


def sanitize_input(value):
    """Sanitize input to prevent SQL injection and XSS."""
    if isinstance(value, str):
        return re.sub(r"[^\w\s-]", "", value.strip())
    return value


@main.route("/")
def index():
    try:
        category = sanitize_input(request.args.get("category", "all"))
        search = sanitize_input(request.args.get("search", ""))
        products = get_items(category, search)
        categories = get_categories()
    except Exception as e:
        flash(f"Error loading products: {str(e)}", "danger")
        return render_template("500.html"), 500
    return render_template(
        "index.html",
        products=products,
        categories=categories,
        selected_category=category,
        search=search,
    )


@main.route("/product/<int:item_id>")
def item_details(item_id):
    try:
        product = get_item(item_id)
        if not product:
            return render_template("404.html"), 404
    except Exception as e:
        flash(f"Error loading product: {str(e)}", "danger")
        return render_template("500.html"), 500
    return render_template("product_details.html", product=product)


@main.route("/basket", methods=["GET", "POST"])
def basket():
    form = BasketForm()

    # Ensure basket exists in session
    if "basket" not in session:
        session["basket"] = []

    basket_items = []
    total = 0

    try:
        for item in session["basket"]:
            product = get_item(item["item_id"])

            if product:
                item_total = product["price"] * item["quantity"]
                basket_items.append(
                    {
                        "item_id": item["item_id"],
                        "name": product["name"],
                        "price": product["price"],
                        "image": product["image"],
                        "category_name": product["category_name"],
                        "quantity": item["quantity"],
                        "total": item_total,
                    }
                )
                total += item_total

        # Handle quantity update
        if form.validate_on_submit():
            item_id = int(request.form.get("item_id"))
            quantity = form.quantity.data

            if quantity < 1:
                flash("Quantity must be at least 1.", "danger")
                return redirect(url_for("main.basket"))

            for item in session["basket"]:
                if item["item_id"] == item_id:
                    item["quantity"] = quantity
                    break

            session.modified = True
            flash("Basket updated.", "success")
            return redirect(url_for("main.basket"))

    except Exception as e:
        flash(f"Error updating basket: {str(e)}", "danger")
        return render_template("500.html"), 500

    return render_template(
        "basket.html", basket_items=basket_items, total=total, form=form
    )


@main.route("/add_to_basket/<int:item_id>", methods=["POST"])
def add_to_basket(item_id):
    try:
        quantity = int(request.form.get("quantity", 1))
        if quantity < 1:
            flash("Quantity must be at least 1.", "danger")
            return redirect(url_for("main.index"))
        if "basket" not in session:
            session["basket"] = []
        for item in session["basket"]:
            if item["item_id"] == item_id:
                item["quantity"] += quantity
                session.modified = True
                flash("Item quantity updated in basket.", "success")
                return redirect(url_for("main.basket"))
        session["basket"].append({"item_id": item_id, "quantity": quantity})
        session.modified = True
        flash("Item added to basket.", "success")
    except ValueError:
        flash("Invalid quantity entered.", "danger")
    except Exception as e:
        flash(f"Error adding to basket: {str(e)}", "danger")
    return redirect(url_for("main.basket"))


@main.route("/remove_from_basket/<int:item_id>")
def remove_from_basket(item_id):
    try:
        if "basket" in session:
            session["basket"] = [
                item for item in session["basket"] if item["item_id"] != item_id
            ]
            session.modified = True
            flash("Item removed from basket.", "success")
    except Exception as e:
        flash(f"Error removing item: {str(e)}", "danger")
    return redirect(url_for("main.basket"))


@main.route("/clear_basket")
def clear_basket():
    try:
        session.pop("basket", None)
        flash("Basket cleared.", "success")
    except Exception as e:
        flash(f"Error clearing basket: {str(e)}", "danger")
    return redirect(url_for("main.basket"))


@main.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "basket" not in session or not session["basket"]:
        flash("Your basket is empty.", "danger")
        return redirect(url_for("main.index"))
    if "user_id" not in session:
        flash("Please log in to checkout.", "danger")
        return redirect(url_for("main.login", next="checkout"))
    form = CheckoutForm()
    basket_items = []
    items_total = 0
    try:
        product = get_item(item["item_id"])
        if product:
            item_total = product["price"] * item["quantity"]
            basket_items.append(
                {
                    "item_id": item["item_id"],
                    "name": product["name"],
                    "category_name": product["category_name"],
                    "price": product["price"],
                    "image": product["image"],
                    "quantity": item["quantity"],
                    "total": item_total,
                }
            )
            items_total += item_total

        delivery_costs = {"standard": 9.50, "express": 12.50, "green": 14.00}
        delivery_option = (
            form.delivery_option.data if form.delivery_option.data else "standard"
        )
        if delivery_option not in delivery_costs:
            flash("Invalid delivery option selected.", "danger")
            return redirect(url_for("main.checkout"))
        delivery_cost = delivery_costs.get(delivery_option, 9.50)
        total = items_total + delivery_cost
        if form.validate_on_submit():
            order_id = create_order(
                sanitize_input(form.full_name.data),
                sanitize_input(form.address.data),
                sanitize_input(form.phone.data),
                delivery_option,
                total,
                session["user_id"],
            )
            for item in basket_items:
                create_order_items(
                    order_id, item["item_id"], item["quantity"], item["price"]
                )

            session.pop("basket", None)
            flash("Order placed successfully!", "success")
            return redirect(url_for("main.index"))
    except Exception as e:
        flash(f"Error placing order: {str(e)}", "danger")
        return render_template("500.html"), 500
    return render_template(
        "checkout.html",
        form=form,
        basket_items=basket_items,
        items_total=items_total,
        delivery_cost=delivery_cost,
        total=total,
        delivery_costs=delivery_costs,
    )


@main.route("/register", methods=["GET", "POST"])
def register():
    user = get_user_session()
    if user:
        flash("You are already logged in", "info")
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = sanitize_input(form.email.data)
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
        except Exception as e:
            flash(f"Error registering user: {str(e)}", "danger")
    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    user = get_user_session()
    if user:
        flash("You are already logged in", "info")
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            user = get_user_by_email(email)
            if user and bcrypt.check_password_hash(user["password"], password):
                session["user"] = user
                session["user_id"] = user["id"]
                session["is_admin"] = True if user["role"] == "admin" else False
                session.permanent = True
                flash("Logged in successfully!", "success")
                next_page = sanitize_input(request.args.get("next", "index"))
                return redirect(url_for(f"main.{next_page}"))
            flash("Invalid username or password.", "danger")
        except Exception as e:
            flash(f"Error logging in: {str(e)}", "danger")

    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    try:
        session.clear()
        flash("Logged out successfully!", "success")
    except Exception as e:
        flash(f"Error logging out: {str(e)}", "danger")
    return redirect(url_for("main.index"))


@main.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def admin():
    form = ProductForm()
    try:
        if form.validate_on_submit():
            create_item(
                sanitize_input(form.name.data),
                form.price.data,
                sanitize_input(form.description.data),
                sanitize_input(form.category.data),
                sanitize_input(form.image.data),
            )

            flash("Product created successfully!", "success")
            return redirect(url_for("main.admin"))
        item_id = request.args.get("item_id", type=int)
        if item_id:
            product = get_item(item_id)
            if product:
                form.name.data = product["name"]
                form.price.data = product["price"]
                form.description.data = product["description"]
                form.category.data = product["category"]
                form.image.data = product["image"]

        products = get_items()
    except Exception as e:
        flash(f"Error managing products: {str(e)}", "danger")
        return render_template("500.html"), 500
    return render_template(
        "admin.html", form=form, products=products, edit_item_id=item_id
    )


@main.route("/admin/delete/<int:item_id>")
@admin_required
def admin_delete(item_id):
    try:
        delete_item(item_id)
        flash("Product deleted.", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "danger")
    return redirect(url_for("main.admin"))


@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@main.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403
