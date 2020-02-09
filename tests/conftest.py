from users import create_app, user_db

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import pytest


@pytest.fixture
def app():
    app = create_app({'TESTING': True})

    # See https://stackoverflow.com/a/36222848/4241180, allows
    # test_client() to work as expected
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app,
                                        {'/metrics': make_wsgi_app()})
    yield app

    # teardown
    user_db.clear()


@pytest.fixture
def client(app):
    yield app.test_client()
