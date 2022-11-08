import os
from consts import INSTANCE_PATH


class Config:
    pass


class ProductionConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/sites/wwwroot/db/dogs.db'
    DATABASE_PATH = os.path.join('/home', 'sites', 'wwwroot', 'db', 'dogs.db')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + INSTANCE_PATH, 'db', 'dogs.db')
    DATABASE_PATH = os.path.join(INSTANCE_PATH, 'db', 'dogs.db')
