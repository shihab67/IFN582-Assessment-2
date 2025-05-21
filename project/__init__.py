from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from project.views import main_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with secure key
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'  # Replace with your MySQL password
    app.config['MYSQL_DB'] = 'grocs'
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Initialize extensions
    Bootstrap5(app)
    app.mysql = MySQL(app)
    Bcrypt(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app