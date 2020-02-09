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

blueprint = Blueprint('Users', __name__, url_prefix='/users')

logger = structlog.get_logger()


@blueprint.route('/', methods=['POST'])
def create_user():
    logger.debug('create_user', data=request.data, form=request.form)
    user_data = request.get_json(force=True)  # TODO: enforce application/json
    logger.debug('create_user', user_data=user_data)
    persisted_user = user_db.new_user(user_data)

    logger.debug('create_user', record=persisted_user)
    return make_response(persisted_user)


@blueprint.route('/', methods=['GET'], defaults={'id': None})
@blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    if id is None:
        return _list_users()

    return _get_user(id)


@blueprint.route('/<id>', methods=['PUT'])
def update_user(id):
    logger.debug('update_user', data=request.data, form=request.form)
    user_data = request.get_json(force=True)

    try:
        updated_user = user_db.update_user(id, user_data)
        if updated_user is None:
            abort(404)

        logger.debug('update_user', updated_user=updated_user)
        return make_response(user_data)
    except user_db.UserIdMismatchException as e:
        logger.warn('update_user', error=e)
        abort(400, e)


@blueprint.route('/<id>', methods=['DELETE'])
def delete_user(id):
    logger.debug('delete_user', user_id=id)

    deleted_user = user_db.delete_user(id)

    if deleted_user is None:
        abort(404)

    return make_response(deleted_user)


def _get_user(id):
    logger.debug('get_user', user_id=id)

    user = user_db.get_user_by_id(id)
    if user is None:
        abort(404)

    logger.debug('get_user', record=user)
    return make_response(user)


def _list_users():
    users = user_db.list_users()
    logger.debug('list_users', user_count=len(users))
    return make_response({'users': users})
