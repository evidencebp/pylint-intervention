# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from flask.helpers import get_env
from fm_database.base import get_session
from fm_database.models.user import User

from fm_api import auth, device, grainbin, user
from fm_api.extensions import cors, jwt, smorest_api


def create_app(config=None, testing=False):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".", maxsplit=1)[0])

    configure_app(app, config, testing)
    register_extensions(app)
    register_blueprints()
    register_errorhandlers()
    register_shellcontext(app)
    register_teardown_request(app)

    return app


def configure_app(app, config=None, testing=False):
    """Set configuration for application."""

    if config:
        app.config.from_object(config)
        return

    # default configuration
    app.config.from_object("fm_api.settings.DevConfig")

    if testing is True:
        # override with testing config
        app.config.from_object("fm_api.settings.TestConfig")
    elif get_env() == "production":
        # override with production config
        app.config.from_object("fm_api.settings.ProdConfig")


def register_extensions(app):
    """Register Flask extensions."""
    smorest_api.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)


def register_blueprints():
    """Register Flask blueprints."""
    smorest_api.register_blueprint(auth.views.blueprint)
    smorest_api.register_blueprint(device.views.blueprint)
    smorest_api.register_blueprint(grainbin.views.blueprint)
    smorest_api.register_blueprint(user.views.blueprint)


def register_errorhandlers():
    """Register error handlers."""


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"User": User}

    app.shell_context_processor(shell_context)


def register_teardown_request(app):
    """Register the teardown context function."""

    def teardown_request(_):
        """The teardown app context function that is called for every request."""

        session = get_session()
        session.remove()

    app.teardown_appcontext(teardown_request)
