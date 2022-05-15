from flask import Flask
from config import config_option
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads

db = SQLAlchemy()
login = LoginManager()
photos = UploadSet('photos', IMAGES)
bootstrap = Bootstrap5()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_option[config_name])

    db.init_app(app)

    login.init_app(app)
    login.login_view = "auth.login"
    login.session_protection = "strong"
    login.login_message_category = "warning"

    bootstrap.init_app(app)
    moment.init_app(app)

    configure_uploads(app, photos)

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth/")

    return app
