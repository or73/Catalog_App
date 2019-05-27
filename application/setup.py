"""
File Path: application/setup.py
Description: setup the App
This will have the function to create the App which will initialize the database and register all blueprints.
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()                # Init SQLAlchemy
login_manager = LoginManager()   # Init LoginManager


def create_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    """ Initialize plugins """

    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth_bp.login'

    # from .modules.user.models import User
    from .modules.user.methods import UserMethod
    @login_manager.user_loader
    def load_user(session_token):
        # def load_user(user_id):
        print('load_user - user_id - session_token: ', session_token)
        print('loading auth...')
        # since the user_id is just the primary key of our auth table, auth it in the query for the auth
        return UserMethod.get_user_session_token(session_token)

    with app.app_context():
        """ Blueprints """
        from .modules.auth.views import auth_bp
        """ Blueprint for Auth routes in App """
        from .modules.catalog.views import catalog_bp
        """ Blueprint for Catalog routes in App """
        from .modules.category.views import category_bp
        """ Blueprint for Category routes in App """
        from .modules.item.views import item_bp
        """ Blueprint for Item routes in App """
        from .modules.user.views import user_bp
        """ Blueprint for User routes in App """

        """" Register Blueprints """
        app.register_blueprint(auth_bp)
        app.register_blueprint(catalog_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(item_bp)
        app.register_blueprint(user_bp)

        from .modules.catalog.models import Catalog
        from .modules.category.models import Category
        from .modules.item.models import Item
        """Import the models so that sqlalchemy can detect them and create the DB """

        db.create_all()
        """ Create the DB """
    return app
