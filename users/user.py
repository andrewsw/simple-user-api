########################################################################
#
# user
#
# This module provides the User blueprint -- all the routes and
# controller-style functionality lives here.
#
########################################################################

from flask import Blueprint, request, make_response, abort
from . import user_db

blueprint = Blueprint('User', __name__, url_prefix='/user')


@blueprint.route('', methods=['POST'])
def create_user():
    user_data = request.get_json(force=True)  # TODO: enforce application/json
    persisted_user = user_db.new_user(user_data)
    return make_response(persisted_user)


@blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    user = user_db.get_user_by_id(id)
    if user is None:
        abort(404)
    return make_response(user)
