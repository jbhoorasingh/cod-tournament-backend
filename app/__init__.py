from flask import Flask
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_praetorian import Praetorian
from .extensions import db, guard, migrate
from flask_cors import CORS
from .commands import create_demo_data, delete_demo_data
from .routes import base
import logging

def create_app(**kwargs):
    app = Flask(__name__)
    #ToDo :: https://github.com/miguelgrinberg/flasky-with-celery/blob/master/app/__init__.py - Implement different configs
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    # Extensions - SQL Alchemy
    #db = SQLAlchemy(app)
    db.init_app(app)
    # Extensions - SQL Alchemy
    migrate.init_app(app, db)
    #migrate = Migrate(app, db)


    from app import models
    # Extensions - Flask Praetorian
    #guard = Praetorian(app, models.User)
    guard.init_app(app, models.User)

    app.cli.add_command(create_demo_data)
    app.cli.add_command(delete_demo_data)
    from app.apis import blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(base, url_prefix='/')
    #app.register_blueprint(apis.api_v1)
    return app


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask