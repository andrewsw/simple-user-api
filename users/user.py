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

import structlog

blueprint = Blueprint('User', __name__, url_prefix='/user')

logger = structlog.get_logger()


@blueprint.route('', methods=['POST'])
def create_user():
    user_data = request.get_json(force=True)  # TODO: enforce application/json
    persisted_user = user_db.new_user(user_data)

    logger.debug('create_user', record=persisted_user)
    return make_response(persisted_user)


@blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    logger.debug('get_user', user_id=id)

    user = user_db.get_user_by_id(id)
    if user is None:
        abort(404)

    logger.debug('get_user', record=user)
    return make_response(user)
