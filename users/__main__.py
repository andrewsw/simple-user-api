import logging
import sys
import structlog

from users import create_app
from werkzeug.serving import run_simple


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

    run_simple(
        'localhost',
        5000,
        create_app(),
        use_reloader=True,
    )


main()
