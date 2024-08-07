from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from . import site_settings
from website.helpers import jobs, backup

db = SQLAlchemy()
DB_NAME = site_settings.DB_NAME
mail = Mail()

def create_app():
    # Site settings
    app = Flask(__name__, static_folder="static")
    app.config['SECRET_KEY'] = site_settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = site_settings.MAIL_SERVER
    app.config['MAIL_USERNAME'] = site_settings.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = site_settings.MAIL_PASSWORD
    app.config['MAIL_PORT'] = site_settings.MAIL_PORT
    app.config['MAIL_USE_SSL'] = site_settings.MAIL_USE_SSL
    app.config['SCHEDULER_API_ENABLED'] = True
    db.init_app(app)
    mail.init_app(app)

    # Load blueprints
    from .pages import pages
    from .authentication import authentication
    from .dashboard import dashboard
    from .explorer import explorer
    from .profile import profile
    from .jinja_templates import jinja_templates

    app.register_blueprint(pages, url_prefix = '/')
    app.register_blueprint(authentication, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(explorer, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(jinja_templates, url_prefix='/')

    @app.context_processor
    def inject_template_scope():
        injections = dict()
        
        def cookies_check():
            value = request.cookies.get('cookie_consent')
            return value == 'true'
        injections.update(cookies_check=cookies_check)

        return injections

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Load error handlers
    from .error_handlers import page_not_found
    app.register_error_handler(404, page_not_found)

    # Create scheduler for background calculations
    scheduler = APScheduler()
    @scheduler.task('interval', id='stats_updater', hours=1)
    def update_stats():
        jobs.update_stats(app)
    @scheduler.task('interval',id='map_updated',hours=1)
    def update_map():
        jobs.update_map(app)
    @scheduler.task('interval', id='remove_inactive_users', hours=24)
    def remove_inactive_users():
        jobs.remove_unused_accounts(app)
    @scheduler.task('interval', id='essay_optimizer_stats', hours=4)
    def update_essay_optimizer_stats():
        jobs.next_historic_interview(app)
    @scheduler.task('interval', id='backup', hours=4)
    def backup_db():
        backup.backup_db()

    scheduler.start()
    # Run calculations on startup if needed
    jobs.update_stats(app)
    # jobs.update_map(app)
    # jobs.remove_unused_accounts(app)
    # jobs.next_historic_interview(app)
    # backup.backup_db()

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print("Created database.")