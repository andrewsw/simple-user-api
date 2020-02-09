# unit tests of the user_db module
from users import user_db
import uuid

user = {
    'given_name': 'Bob',
    'surname': 'Roberts',
    'zip': '12345',
    'email': 'bob@roberts.org'
}


def test_new_user():
    persisted_user = user_db.new_user(user)
    assert persisted_user is not None


def test_new_user_assigns_id():
    user_id = user_db.new_user(user)['id']
    assert user_id is not None
    assert isinstance(user_id, str)
    uuid.UUID(user_id)


def test_get_user():
    persisted_user = user_db.new_user(user)
    user_id = persisted_user['id']
    retrieved_user = user_db.get_user_by_id(user_id)
    assert retrieved_user is not None
    assert retrieved_user == persisted_user


def test_get_user_not_found():
    assert user_db.get_user_by_id(uuid.uuid4()) is None
