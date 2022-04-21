import os


class AppConfig:
    MYSQL_URL = os.getenv("MYSQL_URL")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + MYSQL_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    # github
    GITHUB_API = os.getenv("GITHUB_API")
    GITHUB_USER = os.getenv("GITHUB_USER")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class Configure:
    password_length = [6, 12]
    white_token = ["/login"]
    blank_attr = ["toDict", "_sa_class_manager"]
