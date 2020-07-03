import os
from credentials import *

class Config(object):
    ENV = os.environ.get('APP_ENV') or 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY') or SECRET_KEY
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or 'sqlite:////test.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or 'mysql+pymysql://{}:{}@{}/{}'.format(MYSQL_USER,
                                                                                                     MYSQL_PASSWORD,
                                                                                                     MYSQL_HOST,
                                                                                                     MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_LIFESPAN = {'minutes': 1500}
    JWT_REFRESH_LIFESPAN = {'days': 30}
    # Todo :: work on celery implementation
    #CELERY_BROKER_URL = CELERY_BROKER
    #CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND

