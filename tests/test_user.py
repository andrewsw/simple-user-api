from users.user import REQUIRED_KEYS

import uuid
import json
import pytest


PATH_PREFIX = '/users/'


def test_user_create_works(client, api_user):
    create_response = create_user(client, api_user)
    assert create_response.status_code == 200


def test_user_create_sets_id(client, api_user):
    created_user = create_user(client, api_user).get_json()
    assert created_user.get('id') is not None


def test_user_persistence(client, api_user):
    created_user = create_user(client, api_user).get_json()
    user_id = created_user.get('id')
    get_response = client.get(PATH_PREFIX + user_id)

    assert get_response.status_code == 200

    retrieved_user = get_response.get_json()
    assert created_user == retrieved_user


@pytest.mark.parametrize('missing_key', REQUIRED_KEYS)
def test_user_create_validation(client, api_user, missing_key):
    api_user.pop(missing_key)
    response = create_user(client, api_user)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == 'Bad Request'

    error_message = response_json['error_message']
    assert 'validation' in error_message
    assert 'missing' in error_message
    assert missing_key in error_message


def test_user_create_validation_multiple_missing_keys(client):
    response = create_user(client, {})  # no keys at all!
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == 'Bad Request'

    error_message = response_json['error_message']
    assert 'validation' in error_message
    for key in REQUIRED_KEYS:
        assert key in error_message


def test_user_create_validation_extra_keys(client, api_user):
    api_user['extra'] = 'bogus data'
    response = create_user(client, api_user)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == 'Bad Request'

    error_message = response_json['error_message']
    assert 'validation' in error_message
    assert 'unexpected key' in error_message
    assert 'extra' in error_message


def test_get_user_not_found(client, api_user):
    user_id = gen_user_id()
    response = client.get(PATH_PREFIX + user_id)
    assert response.status_code == 404


def test_update_user(client, api_user):
    user = create_user(client, api_user).get_json()
    user['email'] = 'robert@bob.com'

    response = client.put(PATH_PREFIX + user["id"], json=user)
    assert response.status_code == 200
    updated_user = response.get_json()
    assert updated_user == user


def test_update_user_persistence(client, api_user):
    user = create_user(client, api_user).get_json()
    user['email'] = 'robert@bob.com'
    user_id = user['id']

    response = client.put(PATH_PREFIX + user_id, json=user)
    assert response.status_code == 200

    persisted_user = client.get(PATH_PREFIX + user_id).get_json()
    assert persisted_user == user


def test_update_user_not_found(client, api_user):
    user = create_user(client, api_user).get_json()
    user['email'] = 'robert@bob.com'
    user['id'] = gen_user_id()
    user_id = user['id']

    response = client.put(PATH_PREFIX + user_id, json=user)
    assert response.status_code == 404


def test_update_user_mismatched_id(client, api_user):
    user = create_user(client, api_user).get_json()
    bad_user_id = gen_user_id()

    response = client.put(PATH_PREFIX + bad_user_id, json=user)
    assert response.status_code == 400
    assert 'user_id does not match' in response.json['error_message']


@pytest.mark.parametrize('missing_key', REQUIRED_KEYS + ['id'])
def test_update_user_missing_key(client, api_user, missing_key):
    user = create_user(client, api_user).get_json()
    user_id = user['id']
    user.pop(missing_key)

    response = client.put(PATH_PREFIX + user_id, json=user)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == 'Bad Request'

    error_message = response_json['error_message']
    assert 'validation' in error_message
    assert 'missing' in error_message
    assert missing_key in error_message


def test_update_user_extra_key(client, api_user):
    user = create_user(client, api_user).get_json()
    user['extra'] = 'bogus data'

    response = client.put(PATH_PREFIX + user['id'], json=user)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == 'Bad Request'

    error_message = response_json['error_message']
    assert 'validation' in error_message
    assert 'unexpected key' in error_message
    assert 'extra' in error_message


def test_delete_user(client, api_user):
    user = create_user(client, api_user).get_json()
    user_id = user["id"]

    response = client.delete(PATH_PREFIX + user_id)
    assert response.status_code == 200

    deleted_user = response.get_json()
    assert deleted_user == user

    post_delete_response = client.get(PATH_PREFIX + user_id)
    assert post_delete_response.status_code == 404


def test_delete_user_not_found(client, api_user):
    response = client.delete(PATH_PREFIX + gen_user_id())
    assert response.status_code == 404


def test_list_users(client, api_user):
    first_user = create_user(client, api_user).get_json()
    another_user = json.dumps({
        'given_name': 'Joe',
        'surname': 'Johnson',
        'zip': '12345',
        'email': 'joe@johnson.org'
    })
    second_user = client.post(PATH_PREFIX, data=another_user).get_json()

    response = client.get(PATH_PREFIX)  # bare get should list users
    assert response.status_code == 200

    response_json = response.get_json()
    users = response_json['users']
    assert len(users) == 2
    assert first_user in users
    assert second_user in users


def create_user(client, api_user):
    return client.post(PATH_PREFIX, data=json.dumps(api_user))


def gen_user_id():
    return str(uuid.uuid4())
