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
    SECRET_KEY = 'a secret key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/flaskr'


class ProdConfig(Config):
    ENV = 'production'


configs = {
    'dev': DevConfig,
    'prod': ProdConfig,

    'default': DevConfig
}
