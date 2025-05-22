from flask import Flask
from flask_bootstrap import Bootstrap5
from .db import db
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from project.views import main

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with secure key
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'  # Replace with your MySQL password
    app.config['MYSQL_DB'] = 'grocery_delivery'
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Initialize extensions
    Bootstrap5(app)
    Bcrypt(app)

    csrf.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)

    return app
