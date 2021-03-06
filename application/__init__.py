"""
Flask Application Factory
=========================

Instantiate Flask Application with default confguration
and initialises MongoDB.

"""

from flask import Flask
from flask.templating import render_template
from flask_pymongo import PyMongo
from flask_mail import Mail
from application.config import Config


# Instantiate Mongo Database and assign to variable
mongo = PyMongo()

# Instantiate Flask Mail and assign to variable
mailing = Mail()


def create_app(default_config=Config):
    """
    Creates the application factory, with config
    imported from from Config object in config.py.
    """

    app = Flask(__name__)
    app.config.from_object(default_config)
   

    # Initialise Mongo Database
    mongo.init_app(app)

    # Initialise Flask Mail
    mailing.init_app(app)


    # Import and Register blueprints
    from application.main.views import main as main_bp
    from application.users.views import users as users_bp
    from application.tracks.views import tracks as tracks_bp
    from application.comments.views import comments as comments_bp
    from application.admin.views import admin as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tracks_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(admin_bp)
    

    # Register 404 and 500 error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    return app


def page_not_found(e):
    """
    Returns 404 page in case of invalid
    URL path.
    """
    return render_template("404.html"), 404

def internal_error(e):
    """
    Returns 500 page in case of internal
    server/mongoDB error
    """
    return render_template("500.html"), 500




