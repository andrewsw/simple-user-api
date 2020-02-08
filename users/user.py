from flask import Blueprint, request, make_response

blueprint = Blueprint('User', __name__, url_prefix='/user')


@blueprint.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json(force=True)  # TODO: enforce application/json
    user_data['id'] = 1
    return make_response(user_data)
