class Config:
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


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
