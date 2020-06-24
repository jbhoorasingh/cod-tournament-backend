from flask import url_for, request, jsonify, Blueprint
from app import apis, guard
from flask_praetorian import roles_required, current_user, auth_required, roles_accepted
from app.tasks import add_numbers

base = Blueprint('base', __name__)


@base.route('/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)


@base.route('/celery-test')
def celery_test():
    a = add_numbers.delay(1,2)
    #result = a.wait()
    #print(result)Z
    return "Hello"

@base.route('/protected')
@auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(message='protected endpoint (allowed user {})'.format(
        current_user().username,
    ))


@base.route('/protected_admin_required')
@roles_required('admin')
def protected_admin_required():
    """
    A protected endpoint that requires a role. The roles_required decorator
    will require that the supplied JWT includes the required roles
    .. example::
       $ curl http://localhost:5000/protected_admin_required -X GET \
          -H "Authorization: Bearer <your_token>"
    """
    return jsonify(
        message='protected_admin_required endpoint (allowed user {})'.format(
            current_user().username,
        )
    )


@base.route('/protected_operator_accepted')
@roles_accepted('operator', 'admin')
def protected_operator_accepted():
    """
    A protected endpoint that accepts any of the listed roles. The
    roles_accepted decorator will require that the supplied JWT includes at
    least one of the accepted roles
    .. example::
       $ curl http://localhost/protected_operator_accepted -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(
        message='protected_operator_accepted endpoint (allowed usr {})'.format(
            current_user().username,
        )
    )
