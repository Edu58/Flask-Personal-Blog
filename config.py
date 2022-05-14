class Config:
    UPLOADED_PHOTOS_DEST = 'app/static/photos'


class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'


class ProdConfig(Config):
    DEBUG = False


config_option = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}
