import pytest
from trip_service.refactored import User, Trip, UserNotLoggedInException, _getTripsByUser


def stub_find_trips_by_user(user: User):
    return user.trips

@pytest.fixture
def user() -> User:
    return User()

@pytest.fixture
def friend() -> User:
    return User()

@pytest.fixture
def trip() -> Trip:
    return Trip()


def test_null(user):
    assert(not user.friends)
    assert(not user.trips)


def test_add_friend(user, friend):
    user.addFriend(friend)

    assert(user.getFriends())

def test_is_friends_with(user, friend):
    user.addFriend(friend)

    assert(user.isFriendsWith(friend))


def test_trip(user, trip):
    user.addTrip(trip)

    assert(user.trips == [trip])


def test_get_trip_by_user_as_none(user):
    with pytest.raises(UserNotLoggedInException):
        _getTripsByUser(user,
                        None,
                        stub_find_trips_by_user)


def test_get_trip_by_user_with_no_friend(user, trip):
    not_friend = User()
    user.addTrip(trip)

    res = _getTripsByUser(user,
                          not_friend,
                          stub_find_trips_by_user)

    assert(not res)


def test_get_trip_by_user_with_friend(user, friend, trip):
    user.addFriend(friend)
    user.addTrip(trip)

    res = _getTripsByUser(user,
                          friend,
                          stub_find_trips_by_user)

    assert(res == user.trips)
