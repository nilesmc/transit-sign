# Define the application directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # PSQL/SQL Alchemy Database Config
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRI_MET_APP_ID = os.environ.get('SECRET_KEY')

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/dev_lcd-transit-sign'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_lcd-transit-sign'
    SECRET_KEY = 'this-really-needs-to-be-changed'
