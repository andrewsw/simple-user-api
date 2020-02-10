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

# a valid user record includes all and only these keys
REQUIRED_KEYS = ['given_name', 'surname', 'zip', 'email']


@blueprint.route('/', methods=['POST'])
def create_user():
    logger.debug('create_user', data=request.data, form=request.form)
    user_data = request.get_json(force=True)  # TODO: enforce application/json

    try:
        _validate_new_user(user_data)
        logger.debug('create_user', user_data=user_data)
        persisted_user = user_db.new_user(user_data)

        logger.debug('create_user', record=persisted_user)
        return make_response(persisted_user)
    except ValidationException as e:
        logger.info('create_user', error=e)
        abort(400, e)


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
        _validate_updated_user(user_data)
        updated_user = user_db.update_user(id, user_data)
        if updated_user is None:
            abort(404)

        logger.debug('update_user', updated_user=updated_user)
        return make_response(user_data)
    except (user_db.UserIdMismatchException, ValidationException) as e:
        logger.info('update_user', error=e)
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


def _validate_new_user(user_data):
    _validate_required_keys(user_data, REQUIRED_KEYS)
    _validate_no_extra_keys(user_data, REQUIRED_KEYS)


def _validate_updated_user(user_data):
    _validate_required_keys(user_data, REQUIRED_KEYS + ['id'])
    _validate_no_extra_keys(user_data, REQUIRED_KEYS + ['id'])


def _validate_required_keys(user_data, required_keys):
    missing_keys = [k for k in required_keys if k not in user_data]
    if missing_keys:
        raise ValidationException(f'validation error: required key(s) {missing_keys} are missing')


def _validate_no_extra_keys(user_data, expected_keys):
    input_keys = user_data.keys()
    if len(input_keys) > len(expected_keys):
        extra_keys = [k for k in input_keys if k not in expected_keys]
        raise ValidationException(f'validation error: unexpected key(s) {extra_keys} found')


class ValidationException(Exception):
    pass
