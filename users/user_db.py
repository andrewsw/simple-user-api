########################################################################
#
# user_db
#
# Provides a simple in-memory data store.
#
# Records are keyed by id, a v4 UUID string.  Ids are generated
# automatically on record creation (via new_user).  UUIDs are used to
# prevent adjacent id-based attacks.
#
# No persistence is provided across service instances.  Data dies with
# the process....
#
########################################################################

import uuid

db = {}


def new_user(user):
    """create a new user record from the provided dict

    Arguments:
    user - the user record to create, as a dict

    Returns:
    the newly created user record, with added user id (v4 UUID string)

    """
    id = str(uuid.uuid4())
    user['id'] = id
    db[id] = user
    return user


def get_user_by_id(user_id):
    """gets the user corresponding to the provided user_id

    Arguments:
    user_id: the id of the user to get, a v4 UUID string

    Returns:
    the user, or None if not found

    """
    return db.get(user_id, None)


def update_user(user_id, user_data):
    """updates a pre-existing user record

    Arguments:
    user_id: the id of the user to update
    user_data: the updated user data

    Returns:
    the updated user, or None if the user is not found

    Raises:
    UserIdMismatchException: when the ids don't match...
    """

    if user_id != user_data['id']:
        raise UserIdMismatchException('provided user_id does not match that in provided record')

    orig_user = db.get(user_id, None)

    if orig_user is None:
        return None

    db[user_id] = user_data

    return user_data


def delete_user(user_id):
    """deletes the user record associated with the provided user_id

    Arguments:
    user_id: the v4 uuid string id of the user to delete

    Returns:
    the deleted user record, or None if not found
    """
    return db.pop(user_id, None)


class UserIdMismatchException(Exception):
    pass
