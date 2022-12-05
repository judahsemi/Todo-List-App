import os

from werkzeug import security
from werkzeug.utils import secure_filename



class Config(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SALT_LENGTH = 13
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static/')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SALT_LENGTH = 4
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///%s/data-dev.sqlite' % Config.APPLICATION_DIR


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SALT_LENGTH = 4
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///%s/data-test.sqlite' % Config.APPLICATION_DIR
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "tests.app:5000"


class ProductionConfig(Config):
    DEBUG = False
    SALT_LENGTH = 13
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///%s/data-prod.sqlite' % Config.APPLICATION_DIR


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig}

