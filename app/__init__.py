"""Constructor of the main app."""

import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

# logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', \
#                     level = logging.DEBUG)


def create_app(config_name):
    """Start Flask application."""
    print(f"===> Config name: {config_name}")
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # print(f"===> Logger level: {app.config['LOGGER_LEVEL']}")

    # Enable SQL logging
    app.config["SQLALCHEMY_ECHO"] = True
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    logging.info("========> App setup")

    # setting logging ...
    # app.logger.setLevel(app.config["LOGGER_LEVEL"])
    # handler = logging.FileHandler("logs/northwind.log")
    # app.logger.addHandler(handler)

    # if app.config["SSL_REDIRECT"]:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app
