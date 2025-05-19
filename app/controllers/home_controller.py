from flask import render_template
from ..models import get_items


def index():
    items = get_items()
    print(items, "asdasasd")
    return render_template("home.html", items=items)
