import os
from dotenv import load_dotenv, find_dotenv
import pymysql

load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    RESTPLUS_VALIDATE = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    PAGINATION_COUNT = 20


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
PAGINATION_COUNT = 20
CLOUDINARY_NAME = 'smart_container'
CLOUDINARY_KEY = '594111637396745'
CLOUDINARY_SECRET = 'dWilh8oAELxWIzx3tBJDtus33AQ'
NOTIFICATION_TYPE_PANIC = 1
GOOGLE_MAP_API_KEY ='AIzaSyAv9eE0ODysR4VRO4NkbYMb1sDRrh5CKto'