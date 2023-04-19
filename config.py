from dotenv import load_dotenv
from os import environ as env
import os
import pymysql
import urllib

# Set the default database driver to MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration settings for the Flask app.

    Attributes:
    - db_user: the username for the database
    - db_pass: the password for the database
    - db_host: the host for the database
    - db_port: the port for the database
    - db_name: the name of the database
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - SQLALCHEMY_TRACK_MODIFICATIONS: whether to track modifications to the database
    - SECRET_KEY: the secret key for the app (used for decoding)
    - LOG_FILE_NAME: Log file name
    """

    # Set the connection URI for the database
    # SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"\
    #     or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://tinder_for_food_user:tinder_for_food_password@db/tinder_for_food"
    )

    # Enable tracking modifications to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Set the secret key for the app
    SECRET_KEY = env["SECRET_KEY"]
    LOG_FILE_NAME = "log.txt"
