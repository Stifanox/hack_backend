import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://bite_admin:Admin123@bitehack.postgres.database.azure.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
