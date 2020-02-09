import logging
import sys
import structlog

from users import create_app

from werkzeug.serving import run_simple
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def main():
    logging.basicConfig(
        format='%(message)s',
        stream=sys.stdout,
        level=logging.DEBUG
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.KeyValueRenderer(
                key_order=["event", "request_id"]
            )
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory()
    )

    app = create_app()

    # allows us to view metrics on /metrics
    dispatcher = DispatcherMiddleware(app.wsgi_app,
                                      {'/metrics': make_wsgi_app()})

    run_simple(
        'localhost',
        5000,
        dispatcher,
        use_reloader=True,
    )


main()
