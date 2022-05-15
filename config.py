import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOADED_PHOTOS_DEST = 'app/static/photos'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    uri = os.environ.get("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # rest of connection code using the connection string `uri`
    SQLALCHEMY_DATABASE_URI = uri


config_option = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}
