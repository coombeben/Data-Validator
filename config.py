import os
from consts import INSTANCE_PATH


class Config:
    pass


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///db_share', 'dogs.db')
    DATABASE_PATH = os.path.join('/db_share', 'dogs.db')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + INSTANCE_PATH, 'db', 'dogs.db')
    DATABASE_PATH = os.path.join(INSTANCE_PATH, 'db', 'dogs.db')
