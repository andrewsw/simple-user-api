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
    user_id = gen_user_id()
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 404


def test_update_user(client):
    user = create_user(client).get_json()
    user['email'] = 'robert@bob.com'

    response = client.put(f'/user/{user["id"]}', json=user)
    assert response.status_code == 200
    updated_user = response.get_json()
    assert updated_user == user


def test_update_user_persistence(client):
    user = create_user(client).get_json()
    user['email'] = 'robert@bob.com'
    user_id = user['id']

    response = client.put(f'/user/{user_id}', json=user)
    assert response.status_code == 200

    persisted_user = client.get(f'/user/{user_id}').get_json()
    assert persisted_user == user


def test_update_user_not_found(client):
    user = create_user(client).get_json()
    user['email'] = 'robert@bob.com'
    user['id'] = gen_user_id()
    user_id = user['id']

    response = client.put(f'/user/{user_id}', json=user)
    assert response.status_code == 404


def test_update_user_mismatched_id(client):
    user = create_user(client).get_json()
    bad_user_id = gen_user_id()

    response = client.put(f'/user/{bad_user_id}', json=user)
    assert response.status_code == 400
    assert 'user_id does not match' in response.json['error_message']


def create_user(client):
    return client.post('/user', data=user)


def gen_user_id():
    str(uuid.uuid4())
