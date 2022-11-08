import os
from urllib.parse import quote_plus

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:dogidentifier.database.windows.net,1433;' \
                    f'Database=dogs;Uid=coombeben;Pwd={os.getenv("AZURE_SQL_PASSWORD")};Encrypt=yes;' \
                    f'TrustServerCertificate=no;Connection Timeout=30;'
params = quote_plus(connection_string)


class Config:
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc:///?odbc_connect={params}'


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
