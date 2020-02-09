from flask import make_response

import structlog

logger = structlog.get_logger()


def not_found(error):
    """
    not_found

    Default error handling for not found resources
    """
    logger.warn(error)
    return make_response({'error': 'Not Found'}, 404)


def bad_request(error):
    """
    bad_request

    general purpose bad_request response
    """
    logger.warn(error)

    response = {'error': 'Bad Request'}
    if error.description is not None and error.description.args is not None:
        response['error_message'] = error.description.args[0]  # just grab the first

    return make_response(response, 400)


def register_error_handlers(app):
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found)
