# very basic testing of our app instance -- does it route, and does it
# not route :)


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'


def test_default_404_handler(client):
    response = client.get('/not_ping')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Not Found'


def test_app_user_blueprint_registered(app):
    assert 'User' in app.blueprints


def test_request_id(client):
    response = client.get('/ping')
    assert 'X-Request-ID' in response.headers
