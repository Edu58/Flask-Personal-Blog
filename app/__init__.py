from flask import Flask
from config import config_option
from flask_bootstrap import Bootstrap
from flask_moment import Moment


bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_option[config_name])

    bootstrap.init_app(app)
    moment.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    return app
