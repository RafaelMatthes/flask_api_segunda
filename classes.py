from datetime import datetime

from database_class import UserDatabase, TokenDatabase
from exceptions import UserNotAllowedError
from token_utils import (
    create_custom_token,
    encriptando_jwt,
    encrypt_password,
    encrypt_message,
)


class User:

    def __init__(self, username, password, id=None, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at

    def encrypted_dict(self):
        return {
            "id": encrypt_message(str(self.id)),
            "username": encrypt_message(self.username),
            "created_at": encrypt_message(str(self.created_at))
        }


class Token:

    def __init__(self, code, user:User, created_at=None):
        self.code = code
        self.user = user
        self.created_at = created_at

    @property
    def is_expired(self):

        date_diff = datetime.now() - self.created_at

        # print((date_diff.seconds/60))
        return False if int(date_diff.seconds/60) < 10 else True


class TokenManager(TokenDatabase):

    def _get_token(self, user_id=None, token_code=None):

        try:
            return  [Token(code=item[1], user=item[2], created_at=item[3])
                    for item in self.select(
                    user_id=user_id,
                    token_code=token_code
                    )][0]

        except Exception as err:
            return None

    def get_or_create_token(self, user:User) -> str:

        # pesquisar pelo token do user ou criar um novo e salvar no banco
        # retornar um token válido

        token = self._get_token(user_id=user.id)

        if token and not token.is_expired:
            return token.code

        new_token = create_custom_token()
        self.insert(token_code=new_token, user_id=user.id)

        return new_token


    def verify_token(self, token_code) -> User:

        # verificar se o token informado pertence
        # a um usuário
        # caso True, retornar os dados do User
        # caso False, retornar uma Exception

        token = self._get_token(token_code=token_code)

        if token and not token.is_expired:
            user_manager = UserManager()
            user = user_manager.get_user(id=token.user)
            return encriptando_jwt(user.encrypted_dict())

        raise UserNotAllowedError("Token Inválido")


class UserManager(UserDatabase):

    def add_new_user(self, username, password):

        encripted_pass = encrypt_password(password)

        self.insert(username, encripted_pass)

    def get_user(self, username=None, id=None):

        result_list = self.select(username, id)

        return [
            User(
                id=item[0],
                username=item[1],
                password=item[2],
                created_at=item[3],
            )
           for item in result_list
        ][0]

    def get_user_token(self, username, password):

        try:
            user = self.get_user(username)
            if user.username == username:

                encripted_pass = encrypt_password(password)

                if user.password == encripted_pass:
                    token_creator = TokenManager()
                    return token_creator.get_or_create_token(user=user)

        except:
            pass

        raise UserNotAllowedError("Username ou Password Incorretos")






