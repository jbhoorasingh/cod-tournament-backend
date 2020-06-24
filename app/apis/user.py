from flask_restx import Namespace, Resource, fields, reqparse, inputs
from flask import request
from flask_praetorian import auth_required, current_user
from app import models, db
from app.extensions import guard
from app.core.func import emails, random_generator
from app.tasks import task_send_verification_email
import sqlalchemy
api = Namespace("user", description="User administration related operations")

user = api.model(
    "User",
    {
        "id": fields.String(required=True, description="The user identifier"),
        "firstname": fields.String(required=True, description="The user first name"),
        "lastname": fields.String(required=True, description="The user last name"),
        "username": fields.String(required=True, description="The user email/username"),
        "gender": fields.String(required=True, description="The user gender"),
        "dob": fields.Date(required=False, description="The user date of birth"),
        "registration_date": fields.DateTime(required=False, description="The user date of registration"),
    },
)

create_user = reqparse.RequestParser()
create_user.add_argument("firstname", type=str, required=True, location='json')
create_user.add_argument("lastname", type=str, required=True, location='json')
create_user.add_argument("username", type=str, required=True, location='json')
create_user.add_argument("gender", type=str, required=True, location='json')
create_user.add_argument("password", type=str, required=True, location='json')
create_user.add_argument("dob", type=str, required=True, location='json', help='YYYY-MM-DD')


@api.route("/")

class CurrentUser(Resource):
    @api.doc("get_current_user")
    @api.marshal_list_with(user)
    @auth_required
    def get(self):
        """getcurrent user"""
        user = current_user()
        return user

    @api.doc("create_user")
    @api.marshal_list_with(user)
    @api.expect(create_user)
    @api.doc(security=[])
    def post(self):
        """create a new user"""
        req = request.get_json(force=True)
        try:
            u = models.User(firstname=req['firstname'], lastname=req['lastname'], username=req['username'], dob=req['dob'],
                           gender=req['gender'], password=guard.hash_password(req['password'] ))
        except KeyError:
            api.abort(400, "Required field not present")
        print(req)
        db.session.add(u)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            api.abort(400, "username already exist")
        except:
            db.session.rollback()
            api.abort(500, "Failed to add user to database")

        otp_code = random_generator()
        # Send verification email
        #email = emails.send_verification_email(u.firstname, u.username, otp_code)
        print(otp_code)
        email = task_send_verification_email.delay(u.firstname, u.username, u.id, otp_code)
        print(email)
        #print(email)
        # generate OTP
        # otp = models.UserOTP(code="TEST", user=u, sg_message_id=email['message_id'], type='first')
        # db.session.add(otp)
        # try:
        #     db.session.commit()
        # except:
        #     db.session.rollback()
        #     api.abort(500, "Failed to create otp")

        return u
