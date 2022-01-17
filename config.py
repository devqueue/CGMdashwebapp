"""Flask configuration variables."""
from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY", os.urandom(12).hex())
    FLASK_ENV = environ.get("FLASK_ENV")

    # Database and upload files
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI")
    UPLOAD_FOLDER = environ.get("DATA_PATH")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session config
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    WTF_CSRF_SECRET_KEY = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
