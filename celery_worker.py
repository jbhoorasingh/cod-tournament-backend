from app.extensions import celery
from app import create_app
from app import init_celery
app = create_app()
init_celery(celery, app)