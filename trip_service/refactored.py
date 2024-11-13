from typing import List, Optional, Callable

#
# Exceptions
#
class DependendClassCallDuringUnitTestException(Exception):
  pass

class UserNotLoggedInException(Exception):
  pass

#
# Classes
#
class Trip:
  pass


class User:
  def __init__(self) -> None:
    self.trips: List[Trip] = []
    self.friends: List["User"] = []

  def addFriend(self, user: "User") -> None:
    self.friends.append(user)

  def addTrip(self, trip: Trip) -> None:
    self.trips.append(trip)

  def getFriends(self) -> List["User"]:
    return self.friends

  def isFriendsWith(self, other: "User") -> bool:
    return other in self.friends
#
# Functions
#
def _isUserLoggedIn(user: User) -> bool:
  raise DependendClassCallDuringUnitTestException(
    "_isUserLoggedIn() should not be called in an unit test"
  )

def _getLoggedUser() -> User:
  raise DependendClassCallDuringUnitTestException(
    "_getLoggedUser() should not be called in an unit test"
  )

def _findTripsByUser(user: User) -> List[Trip]:
  raise DependendClassCallDuringUnitTestException(
    "_findTripsByUser() should not be invoked on an unit test."
  )

def getTripsByUser(user: User) -> List[Trip]:
  return _getTripsByUser(user, _getLoggedUser(), _findTripsByUser)

def _getTripsByUser(
  user: User,
  logged_user: Optional[User],
  find_trips_by_user: Callable[[User], List[Trip]]
) -> List[Trip]:

  if not logged_user:
    raise UserNotLoggedInException()

  if user.isFriendsWith(logged_user):
    return find_trips_by_user(user)

  return []
