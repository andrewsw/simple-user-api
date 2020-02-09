import uuid
import json

user = json.dumps({
    'given_name': 'Bob',
    'surname': 'Roberts',
    'zip': '12345',
    'email': 'bob@roberts.org'
})


def test_user_create_works(client):
    create_response = create_user(client)
    assert create_response.status_code == 200


def test_user_create_sets_id(client):
    created_user = create_user(client).get_json()
    assert created_user.get('id') is not None


def test_user_persistence(client):
    created_user = create_user(client).get_json()
    user_id = created_user.get('id')
    get_response = client.get(f'/user/{user_id}')

    assert get_response.status_code == 200

    retrieved_user = get_response.get_json()
    assert created_user == retrieved_user


def test_get_user_not_found(client):
    user_id = str(uuid.uuid4())
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 404


def create_user(client):
    return client.post('/user', data=user)
