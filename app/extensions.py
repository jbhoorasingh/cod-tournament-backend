from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_migrate import Migrate
from celery import Celery

db = SQLAlchemy()
guard = Praetorian()
migrate = Migrate()

def make_celery(app_name=__name__):
    redis_uri = "redis://10.0.0.241:7001"
    return Celery(app_name, backend=redis_uri, broker=redis_uri)

celery = make_celery()