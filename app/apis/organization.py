from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from app import models, db
from flask_praetorian import auth_required, current_user

api = Namespace("organization", description="Tournament related operations")

tournament = api.model(
    "Organizations",
    {
        "id": fields.String(required=True, description="The tournament identifier"),
        "name": fields.String(required=True, description="The tournament name"),
    },
)

create_tournament = reqparse.RequestParser()
create_tournament.add_argument("name", type=str, required=True, location='json')


@api.route("/")
class OrganizationList(Resource):
    @api.doc("list_organizations")
    @api.marshal_list_with(tournament)
    def get(self):
        """List all Families"""
        families = models.Tournament.query.all()
        return families


    @api.doc("create_organization")
    @api.marshal_list_with(tournament)
    @api.expect(create_tournament)
    @auth_required
    def post(self):
        """Create a tournament"""
        req = request.get_json(force=True)
        u = current_user()
        try:
            f = models.Tournament(name=req['name'])
            db.session.add(f)
        except KeyError:
            api.abort(400, "Required field not present")


        try:
            db.session.commit()
        except:
            db.session.rollback()
            api.abort(500, "Failed to commit to database")

        for r in f.roles:
            if r.type == "overlord":
                r.users.append(current_user())

                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    api.abort(500, "failed to add user to role")

        return f


@api.route("/<id>")
@api.param("id", "The o"
                 "'.'"
                 ".;rganization identifier")
@api.response(404, "Organization not found")
class Organization(Resource):
    @api.doc("get_organization")
    @api.marshal_with(tournament)
    def get(self, id):
        """Fetch a Tournament given its identifier"""
        tournament = models.Tournament.query.filter_by(id=id).first()
        if tournament is not None:
            return tournament
        api.abort(404, "Organization not found")

    @api.doc("delete_organization")
    @api.marshal_with(tournament)
    @auth_required
    def delete(self, id):
        """Delete a Tournament given its identifier"""
        tournament = models.Tournament.query.filter_by(id=id).first()
        if tournament is not None:
            if tournament.id in current_user().overlord_of_families:
                print("Current user is authorized")
                db.session.delete(tournament)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    api.abort(500, "Could not delete organization from DB")
                return '', 204
            else:
                api.abort(401, "Unauthorized: user can't delete organization")
        api.abort(404, "Organization not found")

