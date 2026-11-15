from os import environ
from pathlib import Path


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    PRODUCTS_DB = Path(__file__).parent.parent / "data/products.json"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///data.sqlite")
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-key"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///data.sqlite")

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}