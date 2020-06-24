from flask_restx import Namespace, Resource, fields, reqparse, inputs
from flask import request
from flask_praetorian import auth_required, current_user
from app import models, db, guard
from app.core.func import emails, random_generator
import sqlalchemy
api = Namespace("auth", description="Authentication related operation")

token = api.model(
    "Token",
    {
        "access_token": fields.String(required=True, description="The user identifier"),
    },
)

login_parser = reqparse.RequestParser()
login_parser.add_argument("username", type=str, required=True, location='json')
login_parser.add_argument("password", type=str, required=True, location='json')

token_refresh_parser = reqparse.RequestParser()
token_refresh_parser.add_argument("token", type=str, required=True, location='json')


@api.route("/")
class ApiAuthentication(Resource):
    @api.doc("auth_user")
    @api.marshal_list_with(token)
    @api.doc(security=[])
    @api.expect(login_parser)
    def post(self):
        """authenticates user"""
        req = request.get_json(force=True)
        username = req.get('username', None)
        password = req.get('password', None)
        user = guard.authenticate(username, password)
        ret = {'access_token': guard.encode_jwt_token(user)}
        return ret


@api.route("/refresh")
class ApiTokenRefresh(Resource):
    @api.doc("refresh_token")
    @api.marshal_list_with(token)
    @api.doc(security=[])
    @api.expect(token_refresh_parser)
    def post(self):
        """authenticates user"""
        req = request.get_json(force=True)
        token = guard.refresh_jwt_token(req['access_token'])
        ret = {'access_token' : token}
        return ret


