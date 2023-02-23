from database_class import UserDatabase

from exceptions import UserNotAllowedError

class User:

    def __init__(self, username, password, id=None):
        self.id = id
        self.username = username
        self.password = password

class UserManager(UserDatabase):

    def add_new_user(self, username, password):

        self.insert(username, password)

    def get_user(self, username):

        result_list = self.select(username)

        return [
            User(
                id=item[0],
                username=item[1],
                password=item[2]
            )
           for item in result_list
        ]

    def get_or_create_token(self, username, password):

        try:

            user = self.get_user(username)[0]
            if user.username == username:
                if user.password == password:
                    return "!@#!DSADQ!@#!@#"

        except:
            pass

        raise UserNotAllowedError("Username ou Password Incorretos")






