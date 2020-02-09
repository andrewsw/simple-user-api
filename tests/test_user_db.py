# unit tests of the user_db module
from users import user_db

import uuid
import pytest


user_fixture = {
    'given_name': 'Bob',
    'surname': 'Roberts',
    'zip': '12345',
    'email': 'bob@roberts.org'
}


def test_new_user():
    persisted_user = user_db.new_user(user_fixture)
    assert persisted_user is not None


def test_new_user_assigns_id():
    user_id = user_db.new_user(user_fixture)['id']
    assert user_id is not None
    assert isinstance(user_id, str)
    uuid.UUID(user_id)


def test_get_user():
    persisted_user = user_db.new_user(user_fixture)
    user_id = persisted_user['id']
    retrieved_user = user_db.get_user_by_id(user_id)
    assert retrieved_user is not None
    assert retrieved_user == persisted_user


def test_get_user_not_found():
    assert user_db.get_user_by_id(uuid.uuid4()) is None


def test_update_user():
    user = user_db.new_user(user_fixture)
    user['email'] = 'robert@bob.com'
    user_id = user['id']

    updated_user = user_db.update_user(user_id, user)
    assert updated_user == user

    retrieved_user = user_db.get_user_by_id(user_id)
    assert updated_user == retrieved_user


def test_update_user_not_found():
    user = user_db.new_user(user_fixture)
    user['email'] = 'robert@bob.com'
    user['id'] = str(uuid.uuid4())

    updated_user = user_db.update_user(user['id'], user)
    assert updated_user is None


def test_update_user_mismatched_id():
    user = user_db.new_user(user_fixture)
    with pytest.raises(user_db.UserIdMismatchException):
        user_db.update_user(str(uuid.uuid4()), user)


def test_delete_user():
    user = user_db.new_user(user_fixture)
    deleted_user = user_db.delete_user(user['id'])
    assert deleted_user == user

    assert user_db.get_user_by_id(user['id']) is None


def test_delete_user_not_found():
    assert user_db.delete_user(uuid.uuid4()) is None


def test_list_users():
    user1 = user_db.new_user(user_fixture)

    another_user = {
        'given_name': 'Joe',
        'surname': 'Johnson',
        'zip': '12345',
        'email': 'joe@johson.org'
    }
    user2 = user_db.new_user(another_user)

    users = user_db.list_users()

    assert isinstance(users, list)
    assert user1 in users
    assert user2 in users


def test_clear():
    user_db.new_user(user_fixture)
    assert user_db.list_users() != []

    user_db.clear()

    assert user_db.list_users() == []
