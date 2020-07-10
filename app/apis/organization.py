from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from app import models, db
from flask_praetorian import auth_required, current_user

api = Namespace("organization", description="Organization related operations")

organization = api.model(
    "Organizations",
    {
        "id": fields.String(required=True, description="The organization identifier"),
        "name": fields.String(required=True, description="The organization name"),
    },
)

create_organization = reqparse.RequestParser()
create_organization.add_argument("name", type=str, required=True, location='json')


@api.route("/")
class OrganizationList(Resource):
    @api.doc("list_organizations")
    @api.marshal_list_with(organization)
    def get(self):
        """List all Families"""
        families = models.Organization.query.all()
        return families


    @api.doc("create_organization")
    @api.marshal_list_with(organization)
    @api.expect(create_organization)
    @auth_required
    def post(self):
        """Create a organization"""
        req = request.get_json(force=True)
        u = current_user()
        try:
            org = models.Organization(name=req['name'])
            db.session.add(org)
        except KeyError:
            api.abort(400, "Required field not present")


        try:
            db.session.commit()
        except:
            db.session.rollback()
            api.abort(500, "Failed to commit to database")

        for r in org.org_roles:
            if r.type == "admin":
                r.users.append(current_user())

                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    api.abort(500, "failed to add user to role")

        return org


@api.route("/<id>")
@api.param("id", "The organization identifier")
@api.response(404, "Organization not found")
class Organization(Resource):
    @api.doc("get_organization")
    @api.marshal_with(organization)
    def get(self, id):
        """Fetch a organization given its identifier"""
        organization = models.Organization.query.filter_by(id=id).first()
        if organization is not None:
            return organization
        api.abort(404, "Organization not found")

    @api.doc("delete_organization")
    @api.marshal_with(organization)
    @auth_required
    def delete(self, id):
        """Delete a organization given its identifier"""
        organization = models.Organization.query.filter_by(id=id).first()
        if organization is not None:
            if organization.id in current_user().admin_of_orgs:
                print("Current user is authorized")
                db.session.delete(organization)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    api.abort(500, "Could not delete organization from DB")
                return '', 204
            else:
                print(current_user().admin_of_orgs)
                api.abort(401, "Unauthorized: user can't delete organization")
        api.abort(404, "Organization not found")

