from Classes.User import User

class UserManager:
    def __init__(self):
        self._users = []

    def addUser(self, newUser):
        self._users.append(newUser)

    def users(self):
        return self._users

    def makeCopyOfUsers(self):
        return [user for user in self._users]

    def getUser(self, i):
        return self._users[i]

    # def userIterator(self, iterable):
    #     for user in iterable:
    #         yield User(user)