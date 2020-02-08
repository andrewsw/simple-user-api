import json

user = json.dumps({
    'given_name': 'Bob',
    'surname': 'Roberts',
    'zip': '12345',
    'email': 'bob@roberts.org'
})


def test_user_create_works(client):
    create_response = client.post('/user/', data=user)
    assert create_response.status_code == 200


def test_user_create_sets_id(client):
    created_user = client.post('/user/', data=user).get_json()
    assert created_user.get('id') is not None
