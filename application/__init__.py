"""
Flask Application Factory
=========================

Instantiate Flask Application with default confguration
and initialises MongoDB.

"""

from flask import Flask
from flask_pymongo import PyMongo
from application.config import Config

# Instantiate Mongo Database and assign to variable
mongo = PyMongo()

def create_app(default_config=Config):
    """
    Creates the application factory.
    """

    app = Flask(__name__)
    app.config.from_object(default_config)

    # Initialise Mongo Database
    mongo.init_app(app)

    # Import and Register blueprints
    from application.main.views import main as main_bp
    from application.users.views import users as users
    app.register_blueprint(main_bp)
    app.register_blueprint(users)


    return app




