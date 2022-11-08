import os
import urllib.parse

from consts import INSTANCE_PATH

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:dogidentifier.database.windows.net,1433;' \
                    f'Database=dogs;Uid=coombeben;Pwd={os.getenv("AZURE_SQL_PASSWORD")};Encrypt=yes;' \
                    f'TrustServerCertificate=no;Connection Timeout=30;'
params = urllib.parse.quote_plus(connection_string)


class Config:
    pass


class ProductionConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc:///?odbc_connect={params}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + INSTANCE_PATH, 'db', 'dogs.db')
    DATABASE_PATH = os.path.join(INSTANCE_PATH, 'db', 'dogs.db')
