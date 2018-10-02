import os

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "SUPERCARIFLAGILISTICO"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/producto"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/test_db"

class StagingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'staging': StagingConfig,
        'production': ProductionConfig,
}
