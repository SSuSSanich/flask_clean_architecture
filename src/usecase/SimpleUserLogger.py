from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.LoginInformation import LoginInformation
from src.dto.OutputUserCredentials import OutputUserCredentials
from src.exception.PasswordMismatch import PasswordMismatchError
from src.usecase.IPasswordHasher import IPasswordHasher
from src.usecase.IUserLogger import IUserLogger
from src.usecase.IValidator import IValidator


class SimpleUserLogger(IUserLogger):
    def __init__(self, database: IDatabaseGateway, validator: IValidator, password_hasher: IPasswordHasher):
        self.__database = database
        self.__password_hasher = password_hasher
        self.__validator = validator

    def login(self, login_info: LoginInformation) -> OutputUserCredentials:

        self.__validator.check_email(login_info.email)
        self.__validator.check_password(login_info.password)

        password_hash = self.__password_hasher.hash(login_info.password)
        output_user_credentials = self.__database.get_user_by_email_and_pass_hash(login_info.email, password_hash)

        return output_user_credentials
