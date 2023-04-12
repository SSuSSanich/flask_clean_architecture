from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.InputUserCredentials import InputUserCredentials
from src.exception.PasswordMismatch import PasswordMismatchError
from src.usecase.IPasswordHasher import IPasswordHasher
from src.usecase.IUserRegistrar import IUserRegistrar
from src.usecase.IValidator import IValidator


class SimpleUserRegistrar(IUserRegistrar):
    def __init__(self, validator: IValidator, database: IDatabaseGateway, password_hasher: IPasswordHasher):
        self.__validator = validator
        self.__database = database
        self.__password_hasher = password_hasher

    def register(self, user_data: InputUserCredentials) -> None:
        if user_data.password != user_data.retyped_password:
            raise PasswordMismatchError("Password mismatch")

        self.__validator.check_name(user_data.name)
        self.__validator.check_password(user_data.password)
        self.__validator.check_email(user_data.email)

        user_data.password = self.__password_hasher.hash(user_data.password)
        # не очень хорошо, нужен новый dto тк
        # там уже хеш, а не сам пароль, может ввести в заблуждение

        self.__database.save_user_credentials(user_data)