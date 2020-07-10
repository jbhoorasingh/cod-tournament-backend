from flask_restx import Api
from flask import Blueprint
from .tournament import api as tournament_api
from .user import api as user_api
from .auth import api as auth_api
from .organization import api as organization_api


authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api_v1 = Blueprint("apis", __name__, url_prefix="/apis/v1")
blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title="cod-tournament-backend",
          version="1.0",
          description="a simple apis service to manage cod tournaments",
          authorizations=authorization,
          security='apikey')

api.add_namespace(tournament_api)
api.add_namespace(organization_api)
api.add_namespace(user_api)
api.add_namespace(auth_api)


