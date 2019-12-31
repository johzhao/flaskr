from flask import Flask


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app: Flask):
        pass


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://localhost:3306/test'


class ProdConfig(Config):
    ENV = 'production'


configs = {
    'dev': DevConfig,
    'prod': ProdConfig,

    'default': DevConfig
}
