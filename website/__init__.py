from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from . import site_settings

db = SQLAlchemy()
DB_NAME = site_settings.DB_NAME

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = site_settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .pages import pages
    from .authentication import authentication

    app.register_blueprint(pages, url_prefix = '/')
    app.register_blueprint(authentication, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database.")