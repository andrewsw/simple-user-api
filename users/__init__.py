from .error_handlers import register_error_handlers

from flask import Flask, make_response, request
from flask_request_id import RequestID
from flask_prometheus_metrics import register_metrics

from datetime import datetime

import structlog

logger = structlog.get_logger()


def create_app(config=None):

    app = Flask(__name__)

    RequestID(app)

    if config is not None:
        app.config.from_mapping(config)

    # blueprints
    from . import user
    app.register_blueprint(user.blueprint)

    # metrics
    # TODO: proper config
    register_metrics(app, app_version='0.0.1', app_config='development')

    @app.before_request
    def request_id_logger():
        log = logger.new(request_id=request.environ.get('FLASK_REQUEST_ID'))
        log.debug(
            'START',
            method=request.method,
            path=request.full_path,
            time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )

    # simple health check
    @app.route('/ping', methods=['GET'])
    def ping():
        # TODO: implement actual health checks here
        return make_response({'status': 'healthy'})

    register_error_handlers(app)

    return app
