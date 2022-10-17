import ulid
from passlib.hash import pbkdf2_sha256


class Account:
    __id: str
    __email: str
    __hashed_password: str
    __activate: bool

    @staticmethod
    def create_new(email: str, plain_password: str, password_confirm: str) -> 'Account':
        if plain_password != password_confirm:
            # TODO: Validatorクラスを生成して、バリデーションを行うこと
            raise Exception("password err")

        entity = Account()
        entity.__id = ulid.new().str
        entity.__email = email
        entity.__hashed_password = pbkdf2_sha256.hash(plain_password)
        entity.__activate = False
        return entity

    @staticmethod
    def restore(account_id: str, email: str, hashed_password: str, activate: bool) -> 'Account':
        entity = Account()
        entity.__id = account_id
        entity.__email = email
        entity.__hashed_password = hashed_password
        entity.__activate = activate
        return entity

    def change_email(self, new_email: str):
        if self.__email == new_email:
            raise Exception('err change email')
        self.__email = new_email
        self.__activate = False

    def change_password(self, new_password: str, password_confirm: str):
        if new_password != password_confirm:
            # TODO: Validatorクラスを生成して、バリデーションを行うこと
            raise Exception("change password err")
        self.__hashed_password = pbkdf2_sha256.hash(new_password)
        self.__activate = False

    def active(self):
        self.__activate = True

    def serialize(self) -> (str, str, str, bool):
        return self.__id, self.__email, self.__hashed_password, self.__activate
