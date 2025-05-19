# app.py
from flask import Flask, flash, redirect, request
from db import init_db
from session import init_session
from views import register_views
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Initialize DB and session
init_db(app)
init_session(app)

# Register routes/views
register_views(app)


# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    flash(str(e), "danger")
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
