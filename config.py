import os
from consts import INSTANCE_PATH


class Config:
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + INSTANCE_PATH, 'db', 'dogs.db')


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'